import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import selectImageUrl from './select.png'

const WORLD_X_MAX = 500
const WORLD_Y_MAX = 500
const CELL_SIZE = 16
const DEFAULT_VIEWPORT_WIDTH = 896
const DEFAULT_VIEWPORT_HEIGHT = 608
const WORLD_WIDTH = WORLD_X_MAX * CELL_SIZE
const WORLD_HEIGHT = WORLD_Y_MAX * CELL_SIZE
const MIN_ZOOM = 0.1
const MAX_ZOOM = 8
const EDGE_BORDER_COLOR = '#FF1A1A'
const EDGE_BORDER_SCREEN_SIZE = 6

export function runTplace() {
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

	const canvasRef = ref(null)
	const showGrid = ref(false)
	const isToolMenuOpen = ref(false)
	const isPaintMode = ref(false)
	const selectedColor = ref(colors[0].value)
	const pointerStatus = ref('Mouse not here :(')
	const gridLabel = computed(() => 'Show grid')
	const pixelsLeft = ref('100/100')

	const pixels = Array.from({ length: WORLD_Y_MAX }, () => Array.from({ length: WORLD_X_MAX }, () => null))
	const undoStack = []
	const redoStack = []

	let ctx = null
	let hoverImage = null
	let hoverCell = null
	let currentStroke = null
	let isDrawing = false
	let animationFrameId = 0
	let placed = 0
	let cameraX = 0
	let cameraY = 0
	let isPanning = false
	let lastPanX = 0
	let lastPanY = 0
	let touchMode = null
	let lastTouchDistance = 0
	let resizeObserver = null
	let zoom = 1

	function selectColor(color) {
		selectedColor.value = color
	}

	function togglePaintMode() {
		isPaintMode.value = !isPaintMode.value
		isToolMenuOpen.value = isPaintMode.value

		if (!isPaintMode.value) {
			isDrawing = false
			commitStroke()
		}
	}

	function toggleToolMenu() {
		isToolMenuOpen.value = !isToolMenuOpen.value
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
				drawPixel(x, y, pixels[y][x] ?? '#FFFFFF')
			}
		}
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
		if (hoverCell === null || hoverImage === null || !hoverImage.complete) {
			return
		}

		const bounds = getScreenCellBounds(hoverCell.x, hoverCell.y)

		ctx.drawImage(hoverImage, bounds.left, bounds.top, bounds.width, bounds.height)
	}

	function beginStroke() {
		currentStroke = []
	}

	function recordPixelChange(x, y, newColor) {
		const oldColor = pixels[y][x]

		if (oldColor === newColor) {
			return
		}

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

		placed += 1
		pixels[y][x] = newColor
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
			pixels[change.y][change.x] = change.oldColor
		})
		placed = Math.max(0, placed - currentStroke.length)
		currentStroke = null
	}

	function applyStroke(stroke, direction) {
		stroke.forEach((change) => {
			pixels[change.y][change.x] = direction === 'undo' ? change.oldColor : change.newColor
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

	function colorizeCell(cellX, cellY) {
		recordPixelChange(cellX, cellY, selectedColor.value)
	}

	function colorize(event) {
		const pos = getMousePos(event)

		if (pos === null) {
			return
		}

		colorizeCell(pos.cellX, pos.cellY)
	}

	function beginPan(event) {
		event.preventDefault()
		isPanning = true
		isDrawing = false
		commitStroke()

		const { mouseX, mouseY } = getViewportMousePos(event)

		lastPanX = mouseX
		lastPanY = mouseY
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

		touchMode = 'draw'
		isPanning = false
		isDrawing = true
		beginStroke()

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}
		colorizeCell(pos.cellX, pos.cellY)
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
		colorizeCell(pos.cellX, pos.cellY)
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

		if (isDrawing) {
			colorizeCell(pos.cellX, pos.cellY)
		}
	}

	function handleMouseLeave() {
		pointerStatus.value = 'Mouse not here :('
		hoverCell = null
		isDrawing = false
		isPanning = false
		commitStroke()
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

		isDrawing = true
		beginStroke()

		hoverCell = {
			x: pos.cellX,
			y: pos.cellY,
		}

		colorizeCell(pos.cellX, pos.cellY)
	}

	function handleMouseUp(event) {
		if (event.button === 1) {
			isPanning = false
			return
		}

		if (event.button !== 0) {
			return
		}

		if (isPanning) {
			isPanning = false
			return
		}

		isDrawing = false
		commitStroke()
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

	function handleKeydown(event) {
		if (!event.ctrlKey || event.key.toLowerCase() !== 'z') {
			return
		}

		event.preventDefault()

		if (event.shiftKey) {
			redo()
		} else {
			undo()
		}
	}

	function loop() {
		if (!ctx) {
			return
		}

		const canvas = getCanvas()

		ctx.clearRect(0, 0, canvas.width, canvas.height)
		drawPixels()
		drawEdgeBorder()
		drawGrid()
		drawHover()
		pixelsLeft.value = (100 - placed) + '/100'

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
		cancelAnimationFrame(animationFrameId)
		commitStroke()
	})

	return {
		canvasRef,
		colors,
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
		isPaintMode,
		isToolMenuOpen,
		pixelsLeft,
		pointerStatus,
		redo,
		selectColor,
		selectedColor,
		showGrid,
		togglePaintMode,
		toggleToolMenu,
		undo,
	}
}
