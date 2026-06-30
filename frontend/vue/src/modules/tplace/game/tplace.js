import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { getCookie } from '@shared'
import { useUserStore } from '@storage'
import selectImageUrl from './select.png'

const WORLD_X_MAX = 2000
const WORLD_Y_MAX = 2000
const CELL_SIZE = 16
const DEFAULT_VIEWPORT_WIDTH = 896
const DEFAULT_VIEWPORT_HEIGHT = 608
const WORLD_WIDTH = WORLD_X_MAX * CELL_SIZE
const WORLD_HEIGHT = WORLD_Y_MAX * CELL_SIZE
const MIN_ZOOM = 0.2
const MAX_ZOOM = 8
const EDGE_BORDER_COLOR = '#FF1A1A'
const EDGE_BORDER_SCREEN_SIZE = 6
const TPLACE_ROOM_NAME = 'tplace-main'
const DEFAULT_PIXEL_COLOR = '#FFFFFF'
const DESKTOP_CLICK_DRAG_THRESHOLD = 4

export function runTplace() {
	const userStore = useUserStore()
	const colors = [
		{ name: 'Black', value: '#000000' },
		{ name: 'Red', value: '#FF1A1A' },
		{ name: 'Orange', value: '#FF9900' },
		{ name: 'Yellow', value: '#FFFF00' },
		{ name: 'Lime', value: '#CCFF00' },
		{ name: 'Green', value: '#33FF00' },
		{ name: 'Dark Gray', value: '#5A5A5A' },
		{ name: 'Dark Red', value: '#990000' },
		{ name: 'Brown', value: '#804000' },
		{ name: 'Olive', value: '#667700' },
		{ name: 'Dark Green', value: '#1A7F00' },
		{ name: 'Forest', value: '#007F33' },
		{ name: 'Gray', value: '#A0A0A0' },
		{ name: 'Cyan', value: '#1AD4D4' },
		{ name: 'Blue', value: '#1A66FF' },
		{ name: 'Indigo', value: '#4B00FF' },
		{ name: 'Magenta', value: '#CC00FF' },
		{ name: 'Pink', value: '#FF0080' },
		{ name: 'White', value: '#FFFFFF' },
		{ name: 'Teal', value: '#0F7F7A' },
		{ name: 'Navy', value: '#0D3B7F' },
		{ name: 'Deep Blue', value: '#2A0A7F' },
		{ name: 'Purple', value: '#7A0A7F' },
		{ name: 'Dark Pink', value: '#99004D' },
	]

	const colorNameByHex = new Map(colors.map((color) => [normalizeHexColor(color.value), color.name]))
	const unlockedColorValues = new Set()

	const canvasRef = ref(null)
	const showGrid = ref(false)
	const isToolMenuOpen = ref(false)
	const isPaintMode = ref(false)
	const isEraserMode = ref(false)
	const isEyedropperMode = ref(false)
	const isAuthenticated = ref(true)
	const isAuthenticationResolved = ref(false)
	const selectedColor = ref(colors[0].value)
	const pointerStatus = ref('Mouse not here :(')
	const gridLabel = computed(() => 'Show grid')
	const pixelsLeft = ref('0/0')
	const canPaint = computed(() => Number(pixelsLeft.value.split('/')[0]) > 0)
	const regenerationSecondsLeft = ref(0)
	const nyancoins = ref(0)
	const draftPixelCount = ref(0)
	const isLoginRequired = computed(() => isAuthenticationResolved.value && !isAuthenticated.value)
	const loginUrl = computed(() => {
		const currentPath = `${window.location.pathname}${window.location.search}`

		return currentPath === '/' ? '/login' : `/login?next=${encodeURIComponent(currentPath)}`
	})

	let placablePixels = 0
	let maxPlacablePixels = 0
	let nextRegenerationAt = null
	let isCanvasLoaded = false
	let isLoadingProfile = false
	let isCommittingDraft = false

	const pixels = Array.from({ length: WORLD_Y_MAX }, () => Array.from({ length: WORLD_X_MAX }, () => null))
	const undoStack = []
	const redoStack = []

	let ctx = null
	let hoverImage = null
	let hoverCell = null
	let currentStroke = null
	let isDrawing = false
	let animationFrameId = 0
	let cameraX = 0
	let cameraY = 0
	let isPanning = false
	let lastPanX = 0
	let lastPanY = 0
	let isSpacePressed = false
	let pendingPaintClick = null
	let touchMode = null
	let lastTouchDistance = 0
	let resizeObserver = null
	let zoom = 1
	let tplaceSocket = null
	let reconnectTimeoutId = 0
	let reconnectAttempt = 0
	let profileRefreshIntervalId = 0
	let regenerationTimerIntervalId = 0

	const draftPixels = new Map()

	function selectColor(color) {
		const normalized = normalizeHexColor(color)

		if (normalized === null) {
			return false
		}

		isEraserMode.value = false
		isEyedropperMode.value = false
		selectedColor.value = normalized

		return true
	}

	function activateBrushMode() {
		isEraserMode.value = false
		isEyedropperMode.value = false
	}

	function activateEraserMode() {
		isEraserMode.value = true
		isEyedropperMode.value = false
	}

	function activateEyedropperMode() {
		isEraserMode.value = false
		isEyedropperMode.value = true
	}

	function toggleEraserMode() {
		isEraserMode.value = !isEraserMode.value

		if (isEraserMode.value) {
			isEyedropperMode.value = false
		}
	}

	function toggleEyedropperMode() {
		isEyedropperMode.value = !isEyedropperMode.value

		if (isEyedropperMode.value) {
			isEraserMode.value = false
		}
	}

	function togglePaintMode() {
		isPaintMode.value = !isPaintMode.value
		isToolMenuOpen.value = isPaintMode.value

		if (!isPaintMode.value) {
			isDrawing = false
			isPanning = false
			isSpacePressed = false
			pendingPaintClick = null
			isEraserMode.value = false
			isEyedropperMode.value = false
			commitStroke()
		}
	}

	function toggleToolMenu() {
		isToolMenuOpen.value = !isToolMenuOpen.value
	}

	function collapseToolMenuIfQuotaEmpty() {
		if (placablePixels <= 0 && isToolMenuOpen.value) {
			isToolMenuOpen.value = false
			isPaintMode.value = false
		}
	}

	function updatePixelCounter() {
		pixelsLeft.value = `${placablePixels}/${maxPlacablePixels}`
	}

	function updateDraftPixelCount() {
		draftPixelCount.value = draftPixels.size
	}

	function setNyancoins(value) {
		const nextNyancoins = Number(value)

		if (Number.isFinite(nextNyancoins)) {
			nyancoins.value = Math.max(0, nextNyancoins)
		}
	}

	function markAuthenticated() {
		isAuthenticated.value = true
		isAuthenticationResolved.value = true
	}

	function markUnauthenticated() {
		isAuthenticated.value = false
		isAuthenticationResolved.value = true
		userStore.clear()
		unlockedColorValues.clear()
		setPixelQuota(0, 0)
		setNyancoins(0)
		setNextRegeneration(null)
		cancelPaintMode()
	}

	function setPixelQuota(left, max = maxPlacablePixels) {
		const nextLeft = Number(left)
		const nextMax = Number(max)

		if (Number.isFinite(nextLeft)) {
			placablePixels = Math.max(0, nextLeft)
		}

		if (Number.isFinite(nextMax)) {
			maxPlacablePixels = Math.max(0, nextMax)
		}

		updatePixelCounter()
		collapseToolMenuIfQuotaEmpty()
		updateRegenerationTimer()
	}

	function setNextRegeneration(value) {
		const timestamp = Date.parse(value)

		nextRegenerationAt = Number.isFinite(timestamp) ? timestamp : null
		updateRegenerationTimer()
	}

	function updateRegenerationTimer() {
		if (nextRegenerationAt === null || placablePixels >= maxPlacablePixels) {
			regenerationSecondsLeft.value = 0
			return
		}

		const secondsLeft = Math.max(0, Math.ceil((nextRegenerationAt - Date.now()) / 1000))

		regenerationSecondsLeft.value = secondsLeft

		if (secondsLeft === 0 && placablePixels < maxPlacablePixels && !isLoadingProfile) {
			loadTplaceProfile()
		}
	}

	function normalizeHexColor(color) {
		if (typeof color !== 'string') {
			return null
		}

		const normalized = color.trim().toUpperCase()

		if (!/^#[0-9A-F]{6}$/.test(normalized)) {
			return null
		}

		return normalized
	}

	function getColorName(hexColor) {
		const normalized = normalizeHexColor(hexColor)

		if (normalized === null) {
			return null
		}

		return colorNameByHex.get(normalized) ?? null
	}

	function getPixelColor(x, y) {
		return pixels[y]?.[x] ?? DEFAULT_PIXEL_COLOR
	}

	function getVisiblePixelColor(x, y) {
		return draftPixels.get(getDraftKey(x, y))?.newColor ?? getPixelColor(x, y)
	}

	function isColorUnlocked(color) {
		const normalized = normalizeHexColor(color)

		return normalized !== null && unlockedColorValues.has(normalized)
	}

	function pickColorFromCell(x, y) {
		const color = getVisiblePixelColor(x, y)

		if (!isColorUnlocked(color)) {
			pointerStatus.value = 'Color not unlocked'
			return false
		}

		selectColor(color)
		pointerStatus.value = `${getColorName(color) ?? color} picked`

		return true
	}

	function setPixelColor(x, y, color) {
		const normalized = normalizeHexColor(color)

		if (normalized === null || x < 0 || x >= WORLD_X_MAX || y < 0 || y >= WORLD_Y_MAX) {
			return false
		}

		pixels[y][x] = normalized === DEFAULT_PIXEL_COLOR ? null : normalized

		return true
	}

	function applyBackendPixel(pixel) {
		if (!pixel || typeof pixel !== 'object') {
			return false
		}

		const x = Number(pixel.x_pos ?? pixel.x)
		const y = Number(pixel.y_pos ?? pixel.y)
		const color = typeof pixel.color === 'object' ? pixel.color?.hex_code : pixel.color

		if (!Number.isInteger(x) || !Number.isInteger(y)) {
			return false
		}

		return setPixelColor(x, y, color)
	}

	function serializePixelForBroadcast(pixel) {
		if (!pixel || typeof pixel !== 'object') {
			return null
		}

		const x = Number(pixel.x_pos ?? pixel.x)
		const y = Number(pixel.y_pos ?? pixel.y)
		const hexCode = normalizeHexColor(typeof pixel.color === 'object' ? pixel.color?.hex_code : pixel.color)

		if (!Number.isInteger(x) || !Number.isInteger(y) || hexCode === null) {
			return null
		}

		return {
			x_pos: x,
			y_pos: y,
			color: {
				name: typeof pixel.color === 'object' ? pixel.color?.name : getColorName(hexCode),
				hex_code: hexCode,
			},
			updated_at: pixel.updated_at,
		}
	}

	async function readJsonResponse(response) {
		try {
			return await response.json()
		} catch {
			return null
		}
	}

	async function loadCanvas() {
		try {
			const response = await fetch('/api/tplace/canvas/')

			if (!response.ok) {
				throw new Error(`Canvas load failed (${response.status})`)
			}

			const canvas = await response.json()
			const width = Math.min(Number(canvas.width) || WORLD_X_MAX, WORLD_X_MAX)
			const height = Math.min(Number(canvas.height) || WORLD_Y_MAX, WORLD_Y_MAX)
			const palette = canvas.palette ?? {}
			const canvasPixels = Array.isArray(canvas.pixels) ? canvas.pixels : []

			pixels.forEach((row) => row.fill(null))

			if (canvas.encoding === 'sparse') {
				canvasPixels.forEach((pixel) => {
					const x = Number(pixel.x_pos ?? pixel.x)
					const y = Number(pixel.y_pos ?? pixel.y)
					const colorId = pixel.color_id ?? pixel.color
					const color = normalizeHexColor(palette[colorId]) ?? DEFAULT_PIXEL_COLOR

					if (Number.isInteger(x) && Number.isInteger(y)) {
						setPixelColor(x, y, color)
					}
				})
				isCanvasLoaded = true
				return
			}

			for (let y = 0; y < height; y += 1) {
				for (let x = 0; x < width; x += 1) {
					const colorId = canvasPixels[x + y * width]
					const color = normalizeHexColor(palette[colorId]) ?? DEFAULT_PIXEL_COLOR

					setPixelColor(x, y, color)
				}
			}

			isCanvasLoaded = true
		} catch (error) {
			console.error(error)
			pointerStatus.value = 'Canvas load failed'
		}
	}

	async function loadTplaceProfile() {
		if (isLoadingProfile) {
			return
		}

		isLoadingProfile = true

		try {
			const response = await fetch('/api/users/me/tplace/')
			const payload = await readJsonResponse(response)

			if (response.status === 401 || response.status === 403) {
				markUnauthenticated()
				return
			}

			if (!response.ok) {
				return
			}

			markAuthenticated()

			if (Array.isArray(payload?.unlocked_colors)) {
				unlockedColorValues.clear()
				payload.unlocked_colors.forEach((color) => {
					const hexCode = normalizeHexColor(color.hex_code)

					if (hexCode !== null) {
						unlockedColorValues.add(hexCode)
					}

					if (hexCode !== null && color.name) {
						colorNameByHex.set(hexCode, color.name)
					}
				})
			}

			setPixelQuota(payload?.placable_pixels, payload?.max_placable_pixels)
			setNyancoins(payload?.nyancoins)
			setNextRegeneration(payload?.next_regeneration)
		} catch (error) {
			console.error(error)
		} finally {
			isLoadingProfile = false
		}
	}

	function buildTplaceSocketUrl() {
		const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'

		return `${protocol}//${window.location.host}/ws/tplace/${TPLACE_ROOM_NAME}/`
	}

	function connectTplaceSocket() {
		if (tplaceSocket?.readyState === WebSocket.OPEN || tplaceSocket?.readyState === WebSocket.CONNECTING) {
			return
		}

		tplaceSocket = new WebSocket(buildTplaceSocketUrl())

		tplaceSocket.onopen = () => {
			reconnectAttempt = 0

			if (isCanvasLoaded) {
				loadCanvas()
			}
		}

		tplaceSocket.onmessage = handleTplaceSocketMessage
		tplaceSocket.onerror = () => {
			pointerStatus.value = 'Live sync error'
		}
		tplaceSocket.onclose = () => {
			scheduleTplaceReconnect()
		}
	}

	function scheduleTplaceReconnect() {
		clearTimeout(reconnectTimeoutId)

		const delay = Math.min(30000, 1000 * (2 ** reconnectAttempt))
		reconnectAttempt = Math.min(reconnectAttempt + 1, 5)
		reconnectTimeoutId = window.setTimeout(connectTplaceSocket, delay)
	}

	function closeTplaceSocket() {
		clearTimeout(reconnectTimeoutId)

		if (tplaceSocket) {
			tplaceSocket.onclose = null
			tplaceSocket.close()
			tplaceSocket = null
		}
	}

	function handleTplaceSocketMessage(event) {
		let data

		try {
			data = JSON.parse(event.data)
		} catch {
			return
		}

		if (data.type !== 'message' || !data.message?.text) {
			return
		}

		let payload

		try {
			payload = JSON.parse(data.message.text)
		} catch {
			return
		}

		if (payload.kind === 'tplace.pixel') {
			applyBackendPixel(payload.pixel)
		}
	}

	function broadcastPixelChange(pixel) {
		if (tplaceSocket?.readyState !== WebSocket.OPEN) {
			return
		}

		const broadcastPixel = serializePixelForBroadcast(pixel)

		if (broadcastPixel === null) {
			return
		}

		tplaceSocket.send(JSON.stringify({
			message: JSON.stringify({
				kind: 'tplace.pixel',
				pixel: broadcastPixel,
			}),
		}))
	}

	async function sendPixelChange(change) {
		const colorName = getColorName(change.newColor)

		if (colorName === null) {
			throw new Error('Unknown color')
		}

		const response = await fetch('/api/tplace/pixels/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({
				x_pos: change.x,
				y_pos: change.y,
				color: colorName,
			}),
		})
		const payload = await readJsonResponse(response)

		if (!response.ok) {
			throw new Error(payload?.detail ?? `Pixel placement failed (${response.status})`)
		}

		if (payload?.pixel) {
			applyBackendPixel(payload.pixel)
			broadcastPixelChange(payload.pixel)
		}

		setPixelQuota(payload?.placable_pixels, payload?.max_placable_pixels)
		setNyancoins(payload?.nyancoins)
		setNextRegeneration(payload?.next_pixel_at)

		return payload
	}

	function getDraftKey(x, y) {
		return `${x}:${y}`
	}

	function setDraftPixel(x, y, color) {
		const normalizedColor = normalizeHexColor(color)

		if (normalizedColor === null) {
			return false
		}

		const oldColor = getPixelColor(x, y)
		const key = getDraftKey(x, y)

		if (oldColor === normalizedColor) {
			draftPixels.delete(key)
			updateDraftPixelCount()
			return true
		}

		draftPixels.set(key, {
			x,
			y,
			oldColor,
			newColor: normalizedColor,
		})
		updateDraftPixelCount()

		return true
	}

	function eraseDraftPixel(x, y) {
		const key = getDraftKey(x, y)
		const draftPixel = draftPixels.get(key)

		if (!draftPixel) {
			return
		}

		rememberPixelChange(x, y, draftPixel.newColor, draftPixel.oldColor)
		setDraftPixel(x, y, draftPixel.oldColor)
	}

	function recordPixelChange(x, y, newColor) {
		const oldColor = draftPixels.get(getDraftKey(x, y))?.newColor ?? getPixelColor(x, y)
		const normalizedColor = normalizeHexColor(newColor)

		if (normalizedColor === null || oldColor === normalizedColor) {
			return
		}

		if (!draftPixels.has(getDraftKey(x, y)) && draftPixels.size >= placablePixels) {
			pointerStatus.value = 'No paint left'
			return
		}

		rememberPixelChange(x, y, oldColor, normalizedColor)
		setDraftPixel(x, y, normalizedColor)
	}

	function rememberPixelChange(x, y, oldColor, newColor) {
		if (currentStroke === null) {
			currentStroke = []
		}

		const existingChange = currentStroke.find((change) => change.x === x && change.y === y)

		if (existingChange) {
			existingChange.newColor = newColor
		} else {
			currentStroke.push({
				x,
				y,
				oldColor,
				newColor,
			})
		}
	}

	async function confirmDraftPixels() {
		commitStroke()

		if (isCommittingDraft) {
			return
		}

		const changes = Array.from(draftPixels.values())

		if (changes.length === 0) {
			return
		}

		await loadTplaceProfile()

		if (changes.length > placablePixels) {
			pointerStatus.value = `Need ${changes.length} charges`
			return
		}

		isCommittingDraft = true

		try {
			for (const change of changes) {
				await sendPixelChange(change)
				draftPixels.delete(getDraftKey(change.x, change.y))
				updateDraftPixelCount()
			}

			undoStack.length = 0
			redoStack.length = 0
			pointerStatus.value = 'Pixels saved'
		} catch (error) {
			console.error(error)
			pointerStatus.value = error.message || 'Pixel placement failed'
			loadTplaceProfile()
		} finally {
			isCommittingDraft = false
		}
	}

	function cancelDraftPixels() {
		draftPixels.clear()
		updateDraftPixelCount()
		undoStack.length = 0
		redoStack.length = 0
		currentStroke = null
	}

	function cancelPaintMode() {
		isEraserMode.value = false
		isEyedropperMode.value = false
		isDrawing = false
		isPanning = false
		isSpacePressed = false
		pendingPaintClick = null
		touchMode = null
		hoverCell = null
		cancelDraftPixels()
		isPaintMode.value = false
		isToolMenuOpen.value = false
	}

	function clamp(value, min, max) {
		return Math.max(min, Math.min(max, value))
	}

	function getScreenCellSize() {
		return CELL_SIZE * zoom
	}

	function getViewportDimensions() {
		const canvas = canvasRef.value

		if (!(canvas instanceof HTMLCanvasElement) || canvas.width === 0 || canvas.height === 0) {
			return {
				width: DEFAULT_VIEWPORT_WIDTH,
				height: DEFAULT_VIEWPORT_HEIGHT,
			}
		}

		return {
			width: canvas.width,
			height: canvas.height,
		}
	}

	function getVisibleWorldSize() {
		const { width, height } = getViewportDimensions()

		return {
			width: width / zoom,
			height: height / zoom,
		}
	}

	function getEdgeBorderWorldSize() {
		return EDGE_BORDER_SCREEN_SIZE / zoom
	}

	function clampCamera() {
		const { width, height } = getVisibleWorldSize()
		const borderSize = getEdgeBorderWorldSize()

		cameraX = Math.round(clamp(cameraX, -borderSize, Math.max(-borderSize, WORLD_WIDTH - width + borderSize)))
		cameraY = Math.round(clamp(cameraY, -borderSize, Math.max(-borderSize, WORLD_HEIGHT - height + borderSize)))
	}

	function getCanvas() {
		if (!(canvasRef.value instanceof HTMLCanvasElement)) {
			throw new Error('Canvas not found')
		}

		return canvasRef.value
	}

	function getViewportPoint(clientX, clientY) {
		const canvas = getCanvas()
		const rect = canvas.getBoundingClientRect()
		const style = getComputedStyle(canvas)

		const borderLeft = parseFloat(style.borderLeftWidth)
		const borderTop = parseFloat(style.borderTopWidth)
		const borderRight = parseFloat(style.borderRightWidth)
		const borderBottom = parseFloat(style.borderBottomWidth)
		const drawableWidth = Math.max(1, rect.width - borderLeft - borderRight)
		const drawableHeight = Math.max(1, rect.height - borderTop - borderBottom)
		const scaleX = canvas.width / drawableWidth
		const scaleY = canvas.height / drawableHeight
		const mouseX = (clientX - rect.left - borderLeft) * scaleX
		const mouseY = (clientY - rect.top - borderTop) * scaleY

		return { mouseX, mouseY }
	}

	function getViewportMousePos(event) {
		return getViewportPoint(event.clientX, event.clientY)
	}

	function getTouchViewportPos(touch) {
		return getViewportPoint(touch.clientX, touch.clientY)
	}

	function getCellFromViewportPos(mouseX, mouseY) {
		const worldX = cameraX + mouseX / zoom
		const worldY = cameraY + mouseY / zoom

		if (worldX < 0 || worldX >= WORLD_WIDTH || worldY < 0 || worldY >= WORLD_HEIGHT) {
			pointerStatus.value = 'Border'

			return null
		}

		const cellX = clamp(Math.floor(worldX / CELL_SIZE), 0, WORLD_X_MAX - 1)
		const cellY = clamp(Math.floor(worldY / CELL_SIZE), 0, WORLD_Y_MAX - 1)

		pointerStatus.value = `Mouse pos (x,y): ${cellX},${cellY}`

		return { cellX, cellY }
	}

	function getMousePos(event) {
		const { mouseX, mouseY } = getViewportMousePos(event)

		return getCellFromViewportPos(mouseX, mouseY)
	}

	function getTouchPos(touch) {
		const { mouseX, mouseY } = getTouchViewportPos(touch)

		return getCellFromViewportPos(mouseX, mouseY)
	}

	function syncCanvasSize(centerCamera = false) {
		const canvas = getCanvas()
		const nextWidth = Math.max(1, Math.floor(canvas.clientWidth))
		const nextHeight = Math.max(1, Math.floor(canvas.clientHeight))

		if (canvas.width !== nextWidth || canvas.height !== nextHeight) {
			canvas.width = nextWidth
			canvas.height = nextHeight
		}

		if (ctx) {
			ctx.imageSmoothingEnabled = false
		}

		if (centerCamera) {
			cameraX = (WORLD_WIDTH - canvas.width / zoom) / 2
			cameraY = (WORLD_HEIGHT - canvas.height / zoom) / 2
		}

		clampCamera()
	}

	function getScreenCellBounds(x, y) {
		const left = Math.floor((x * CELL_SIZE - cameraX) * zoom)
		const top = Math.floor((y * CELL_SIZE - cameraY) * zoom)
		const right = Math.ceil((((x + 1) * CELL_SIZE) - cameraX) * zoom)
		const bottom = Math.ceil((((y + 1) * CELL_SIZE) - cameraY) * zoom)

		return {
			left,
			top,
			width: Math.max(1, right - left),
			height: Math.max(1, bottom - top),
		}
	}

	function drawPixel(x, y, color) {
		const bounds = getScreenCellBounds(x, y)

		ctx.fillStyle = color
		ctx.fillRect(bounds.left, bounds.top, bounds.width, bounds.height)
	}

	function drawEdgeBorder() {
		const left = Math.floor((0 - cameraX) * zoom)
		const top = Math.floor((0 - cameraY) * zoom)
		const right = Math.ceil((WORLD_WIDTH - cameraX) * zoom)
		const bottom = Math.ceil((WORLD_HEIGHT - cameraY) * zoom)
		const width = Math.max(0, right - left)
		const height = Math.max(0, bottom - top)
		const borderSize = EDGE_BORDER_SCREEN_SIZE

		ctx.fillStyle = EDGE_BORDER_COLOR
		ctx.fillRect(left - borderSize, top - borderSize, borderSize, height + borderSize * 2)
		ctx.fillRect(right, top - borderSize, borderSize, height + borderSize * 2)
		ctx.fillRect(left, top - borderSize, width, borderSize)
		ctx.fillRect(left, bottom, width, borderSize)
	}

	function drawPixels() {
		const { width, height } = getVisibleWorldSize()
		const firstX = clamp(Math.floor(cameraX / CELL_SIZE), 0, WORLD_X_MAX - 1)
		const firstY = clamp(Math.floor(cameraY / CELL_SIZE), 0, WORLD_Y_MAX - 1)
		const lastX = clamp(Math.ceil((cameraX + width) / CELL_SIZE), 0, WORLD_X_MAX - 1)
		const lastY = clamp(Math.ceil((cameraY + height) / CELL_SIZE), 0, WORLD_Y_MAX - 1)

		for (let y = firstY; y <= lastY; y += 1) {
			for (let x = firstX; x <= lastX; x += 1) {
				drawPixel(x, y, pixels[y][x] ?? DEFAULT_PIXEL_COLOR)
			}
		}
	}

	function drawHoverMarker(x, y) {
		if (hoverImage === null || !hoverImage.complete) {
			return
		}

		const bounds = getScreenCellBounds(x, y)

		ctx.drawImage(hoverImage, bounds.left, bounds.top, bounds.width, bounds.height)
	}

	function drawDraftPixels() {
		draftPixels.forEach((change) => {
			drawPixel(change.x, change.y, change.newColor)
			drawHoverMarker(change.x, change.y)
		})
	}

	function drawGrid() {
		if (!showGrid.value) {
			return
		}

		const canvas = getCanvas()
		const { width, height } = getVisibleWorldSize()
		const firstX = Math.max(0, Math.floor(cameraX / CELL_SIZE))
		const firstY = Math.max(0, Math.floor(cameraY / CELL_SIZE))
		const lastX = Math.min(WORLD_X_MAX, Math.ceil((cameraX + width) / CELL_SIZE))
		const lastY = Math.min(WORLD_Y_MAX, Math.ceil((cameraY + height) / CELL_SIZE))

		ctx.strokeStyle = '#A0A0A0'
		ctx.lineWidth = 1

		for (let x = firstX; x <= lastX; x += 1) {
			const screenX = Math.round((x * CELL_SIZE - cameraX) * zoom) + 0.5

			ctx.beginPath()
			ctx.moveTo(screenX, 0)
			ctx.lineTo(screenX, canvas.height)
			ctx.stroke()
		}

		for (let y = firstY; y <= lastY; y += 1) {
			const screenY = Math.round((y * CELL_SIZE - cameraY) * zoom) + 0.5

			ctx.beginPath()
			ctx.moveTo(0, screenY)
			ctx.lineTo(canvas.width, screenY)
			ctx.stroke()
		}
	}

	function drawHover() {
		if (hoverCell === null) {
			return
		}

		drawHoverMarker(hoverCell.x, hoverCell.y)
	}

	function beginStroke() {
		currentStroke = []
	}

	function commitStroke() {
		if (currentStroke === null) {
			return
		}

		if (currentStroke.length > 0) {
			undoStack.push(currentStroke)
			redoStack.length = 0
		}

		currentStroke = null
	}

	function cancelStroke() {
		if (currentStroke === null) {
			return
		}

		currentStroke.forEach((change) => {
			setDraftPixel(change.x, change.y, change.oldColor)
		})
		currentStroke = null
	}

	function applyStroke(stroke, direction) {
		stroke.forEach((change) => {
			const nextColor = direction === 'undo' ? change.oldColor : change.newColor

			setDraftPixel(change.x, change.y, nextColor)
		})
	}

	function undo() {
		commitStroke()

		const stroke = undoStack.pop()

		if (!stroke) {
			return
		}

		applyStroke(stroke, 'undo')
		redoStack.push(stroke)
	}

	function redo() {
		commitStroke()

		const stroke = redoStack.pop()

		if (!stroke) {
			return
		}

		applyStroke(stroke, 'redo')
		undoStack.push(stroke)
	}

	function applyActiveToolToCell(cellX, cellY) {
		if (isEyedropperMode.value) {
			pickColorFromCell(cellX, cellY)
		} else if (isEraserMode.value) {
			eraseDraftPixel(cellX, cellY)
		} else {
			recordPixelChange(cellX, cellY, selectedColor.value)
		}
	}

	function clearPendingPaintClick() {
		pendingPaintClick = null
	}

	function endKeyboardPaintStroke() {
		if (!isDrawing) {
			return
		}

		isDrawing = false
		commitStroke()
	}

	function paintWithActiveTool(cellX, cellY) {
		if (isEyedropperMode.value) {
			pickColorFromCell(cellX, cellY)
			isSpacePressed = false
			return
		}

		if (!isDrawing) {
			isDrawing = true
			beginStroke()
		}

		applyActiveToolToCell(cellX, cellY)
	}

	function beginPanAt(mouseX, mouseY) {
		isPanning = true
		isDrawing = false
		pendingPaintClick = null
		commitStroke()
		lastPanX = mouseX
		lastPanY = mouseY
	}

	function beginPan(event) {
		event.preventDefault()

		const { mouseX, mouseY } = getViewportMousePos(event)

		beginPanAt(mouseX, mouseY)
	}

	function panCameraTo(mouseX, mouseY) {
		const deltaX = mouseX - lastPanX
		const deltaY = mouseY - lastPanY

		cameraX -= deltaX / zoom
		cameraY -= deltaY / zoom
		clampCamera()

		lastPanX = mouseX
		lastPanY = mouseY
		pointerStatus.value = `Camera (x,y): ${Math.round(cameraX)},${Math.round(cameraY)}`
	}

	function panCamera(event) {
		const { mouseX, mouseY } = getViewportMousePos(event)

		panCameraTo(mouseX, mouseY)
	}

	function zoomAtViewportPoint(mouseX, mouseY, nextZoom) {
		const clampedZoom = clamp(nextZoom, MIN_ZOOM, MAX_ZOOM)

		if (clampedZoom === zoom) {
			return false
		}

		const worldXBeforeZoom = cameraX + mouseX / zoom
		const worldYBeforeZoom = cameraY + mouseY / zoom

		zoom = clampedZoom
		cameraX = worldXBeforeZoom - mouseX / zoom
		cameraY = worldYBeforeZoom - mouseY / zoom
		clampCamera()

		return true
	}

	function handleWheel(event) {
		event.preventDefault()

		const { mouseX, mouseY } = getViewportMousePos(event)
		const zoomFactor = event.deltaY < 0 ? 1.1 : 1 / 1.1

		if (zoomAtViewportPoint(mouseX, mouseY, zoom * zoomFactor)) {
			pointerStatus.value = `Zoom: ${Math.round(zoom * 100)}%`
		}
	}

	function getTouchGesture(touches) {
		const first = getTouchViewportPos(touches[0])
		const second = getTouchViewportPos(touches[1])
		const deltaX = second.mouseX - first.mouseX
		const deltaY = second.mouseY - first.mouseY

		return {
			centerX: (first.mouseX + second.mouseX) / 2,
			centerY: (first.mouseY + second.mouseY) / 2,
			distance: Math.hypot(deltaX, deltaY),
		}
	}

	function beginTouchPan(touch) {
		const { mouseX, mouseY } = getTouchViewportPos(touch)

		touchMode = 'pan'
		isPanning = true
		isDrawing = false
		hoverCell = null
		commitStroke()
		lastPanX = mouseX
		lastPanY = mouseY
	}

	function beginTouchDraw(touch) {
		const pos = getTouchPos(touch)

		if (pos === null) {
			hoverCell = null
			return
		}

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}

		if (isEyedropperMode.value) {
			pickColorFromCell(pos.cellX, pos.cellY)
			return
		}

		touchMode = 'draw'
		isPanning = false
		isDrawing = true
		beginStroke()
		applyActiveToolToCell(pos.cellX, pos.cellY)
	}

	function beginTouchPanZoom(touches) {
		const gesture = getTouchGesture(touches)

		if (touchMode === 'draw') {
			cancelStroke()
		} else {
			commitStroke()
		}

		touchMode = 'pan-zoom'
		isPanning = true
		isDrawing = false
		hoverCell = null
		lastPanX = gesture.centerX
		lastPanY = gesture.centerY
		lastTouchDistance = gesture.distance
	}

	function updateTouchDraw(touch) {
		const pos = getTouchPos(touch)

		if (pos === null) {
			hoverCell = null
			return
		}

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}
		applyActiveToolToCell(pos.cellX, pos.cellY)
	}

	function updateTouchPanZoom(touches) {
		const gesture = getTouchGesture(touches)

		if (lastTouchDistance > 0 && gesture.distance > 0) {
			zoomAtViewportPoint(
				gesture.centerX,
				gesture.centerY,
				zoom * (gesture.distance / lastTouchDistance),
			)
		}

		panCameraTo(gesture.centerX, gesture.centerY)
		lastTouchDistance = gesture.distance
		pointerStatus.value = `Camera (x,y): ${Math.round(cameraX)},${Math.round(cameraY)} Zoom: ${Math.round(zoom * 100)}%`
	}

	function handleMouseMove(event) {
		if (isPaintMode.value && isSpacePressed) {
			event.preventDefault()
			isPanning = false
			clearPendingPaintClick()

			const pos = getMousePos(event)

			if (pos === null) {
				hoverCell = null
				return
			}

			hoverCell = {
				x: pos.cellX,
				y: pos.cellY,
			}
			paintWithActiveTool(pos.cellX, pos.cellY)
			return
		}

		if (isPanning) {
			panCamera(event)
			return
		}

		const pos = getMousePos(event)

		if (pos === null) {
			hoverCell = null
			return
		}

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}

		if (pendingPaintClick !== null) {
			const { mouseX, mouseY } = getViewportMousePos(event)
			const movedDistance = Math.hypot(mouseX - pendingPaintClick.mouseX, mouseY - pendingPaintClick.mouseY)

			if (movedDistance > DESKTOP_CLICK_DRAG_THRESHOLD) {
				event.preventDefault()

				const panStart = pendingPaintClick

				clearPendingPaintClick()
				beginPanAt(panStart.mouseX, panStart.mouseY)
				panCameraTo(mouseX, mouseY)
			}

			return
		}
	}

	function handleMouseLeave() {
		pointerStatus.value = 'Mouse not here :('
		hoverCell = null
		clearPendingPaintClick()
		isPanning = false
		endKeyboardPaintStroke()
	}

	function handleMouseDown(event) {
		if (event.button === 1) {
			beginPan(event)
			return
		}

		if (event.button !== 0) {
			return
		}

		if (!isPaintMode.value) {
			beginPan(event)
			return
		}

		event.preventDefault()

		const pos = getMousePos(event)

		if (pos === null) {
			hoverCell = null
			return
		}

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}

		if (isSpacePressed) {
			paintWithActiveTool(pos.cellX, pos.cellY)
			return
		}

		const { mouseX, mouseY } = getViewportMousePos(event)

		isPanning = false
		isDrawing = false
		commitStroke()
		pendingPaintClick = {
			mouseX,
			mouseY,
			cellX: pos.cellX,
			cellY: pos.cellY,
		}
	}

	function handleMouseUp(event) {
		if (event.button === 1) {
			isPanning = false
			return
		}

		if (event.button !== 0) {
			return
		}

		if (pendingPaintClick !== null) {
			event.preventDefault()

			const click = pendingPaintClick
			const pos = getMousePos(event)
			const cellX = pos?.cellX ?? click.cellX
			const cellY = pos?.cellY ?? click.cellY

			if (pos !== null) {
				hoverCell = {
					x: pos.cellX,
					y: pos.cellY,
				}
			}

			clearPendingPaintClick()
			paintWithActiveTool(cellX, cellY)
			endKeyboardPaintStroke()
			return
		}

		if (isPanning) {
			isPanning = false
			return
		}

		if (!isSpacePressed) {
			endKeyboardPaintStroke()
		}
	}

	function handleTouchStart(event) {
		event.preventDefault()

		if (event.touches.length >= 2) {
			beginTouchPanZoom(event.touches)
			return
		}

		if (event.touches.length !== 1) {
			return
		}

		if (isPaintMode.value) {
			beginTouchDraw(event.touches[0])
		} else {
			beginTouchPan(event.touches[0])
		}
	}

	function handleTouchMove(event) {
		event.preventDefault()

		if (event.touches.length >= 2) {
			if (touchMode !== 'pan-zoom') {
				beginTouchPanZoom(event.touches)
			} else {
				updateTouchPanZoom(event.touches)
			}
			return
		}

		if (event.touches.length !== 1) {
			return
		}

		if (touchMode === 'draw') {
			updateTouchDraw(event.touches[0])
		} else if (touchMode === 'pan') {
			const { mouseX, mouseY } = getTouchViewportPos(event.touches[0])

			panCameraTo(mouseX, mouseY)
		}
	}

	function handleTouchEnd(event) {
		event.preventDefault()

		if (event.touches.length >= 2) {
			beginTouchPanZoom(event.touches)
			return
		}

		if (touchMode === 'pan-zoom' && event.touches.length === 1 && !isPaintMode.value) {
			beginTouchPan(event.touches[0])
			return
		}

		if (event.touches.length === 0) {
			isDrawing = false
			isPanning = false
			touchMode = null
			lastTouchDistance = 0
			commitStroke()
		}
	}

	function handleTouchCancel(event) {
		event.preventDefault()
		isDrawing = false
		isPanning = false
		touchMode = null
		lastTouchDistance = 0
		hoverCell = null
		commitStroke()
	}

	function preventMiddleClick(event) {
		if (event.button === 1) {
			event.preventDefault()
		}
	}

	function isShortcutInputTarget(target) {
		if (!(target instanceof HTMLElement)) {
			return false
		}

		return target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)
	}

	function handleKeydown(event) {
		const key = event.key.toLowerCase()
		const isUndoRedoShortcut = (event.ctrlKey || event.metaKey) && !event.altKey && key === 'z'

		if (isUndoRedoShortcut) {
			event.preventDefault()

			if (event.shiftKey) {
				redo()
			} else {
				undo()
			}
			return
		}

		if (isShortcutInputTarget(event.target) || event.ctrlKey || event.metaKey || event.altKey || !isPaintMode.value) {
			return
		}

		if (event.code === 'Space') {
			event.preventDefault()

			if (!event.repeat) {
				isSpacePressed = true
				isPanning = false
				clearPendingPaintClick()
			}
			return
		}

		switch (key) {
		case 'e':
			event.preventDefault()
			activateEraserMode()
			break
		case 'q':
			event.preventDefault()
			activateBrushMode()
			break
		case 'f':
			event.preventDefault()
			activateEyedropperMode()
			break
		case 'escape':
			event.preventDefault()
			cancelPaintMode()
			break
		case 'x':
			event.preventDefault()
			toggleToolMenu()
			break
		case 'g':
			event.preventDefault()
			showGrid.value = !showGrid.value
			break
		case 'enter':
			event.preventDefault()
			confirmDraftPixels()
			break
		default:
			break
		}
	}

	function handleKeyup(event) {
		if (event.code !== 'Space') {
			return
		}

		if (isPaintMode.value) {
			event.preventDefault()
		}

		isSpacePressed = false
		endKeyboardPaintStroke()
	}

	function handleWindowBlur() {
		isSpacePressed = false
		isPanning = false
		clearPendingPaintClick()
		endKeyboardPaintStroke()
	}

	function loop() {
		if (!ctx) {
			return
		}

		const canvas = getCanvas()

		ctx.clearRect(0, 0, canvas.width, canvas.height)
		drawPixels()
		drawDraftPixels()
		drawEdgeBorder()
		drawGrid()
		drawHover()

		animationFrameId = requestAnimationFrame(loop)
	}

	onMounted(() => {
		const canvas = getCanvas()
		ctx = canvas.getContext('2d')

		if (!ctx) {
			throw new Error('2D context not available')
		}

		ctx.imageSmoothingEnabled = false
		syncCanvasSize(true)

		hoverImage = new Image()
		hoverImage.src = selectImageUrl

		resizeObserver = new ResizeObserver(() => {
			syncCanvasSize(false)
		})
		resizeObserver.observe(canvas)

		canvas.addEventListener('auxclick', preventMiddleClick)
		document.addEventListener('keydown', handleKeydown)
		document.addEventListener('keyup', handleKeyup)
		window.addEventListener('blur', handleWindowBlur)
		updatePixelCounter()
		loadCanvas()
		loadTplaceProfile()
		connectTplaceSocket()
		profileRefreshIntervalId = window.setInterval(loadTplaceProfile, 30000)
		regenerationTimerIntervalId = window.setInterval(updateRegenerationTimer, 1000)
		loop()
	})

	onBeforeUnmount(() => {
		const canvas = canvasRef.value

		if (canvas instanceof HTMLCanvasElement) {
			canvas.removeEventListener('auxclick', preventMiddleClick)
		}

		resizeObserver?.disconnect()
		resizeObserver = null

		document.removeEventListener('keydown', handleKeydown)
		document.removeEventListener('keyup', handleKeyup)
		window.removeEventListener('blur', handleWindowBlur)
		clearInterval(profileRefreshIntervalId)
		clearInterval(regenerationTimerIntervalId)
		closeTplaceSocket()
		cancelAnimationFrame(animationFrameId)
		commitStroke()
	})

	return {
		cancelPaintMode,
		canPaint,
		canvasRef,
		colors,
		confirmDraftPixels,
		draftPixelCount,
		gridLabel,
		handleMouseDown,
		handleMouseLeave,
		handleMouseMove,
		handleMouseUp,
		handleTouchCancel,
		handleTouchEnd,
		handleTouchMove,
		handleTouchStart,
		handleWheel,
		isEraserMode,
		isEyedropperMode,
		isLoginRequired,
		isPaintMode,
		isToolMenuOpen,
		loginUrl,
		nyancoins,
		pixelsLeft,
		pointerStatus,
		redo,
		regenerationSecondsLeft,
		selectColor,
		selectedColor,
		showGrid,
		toggleEraserMode,
		toggleEyedropperMode,
		togglePaintMode,
		toggleToolMenu,
		undo,
	}
}
