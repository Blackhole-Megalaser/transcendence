import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import selectImageUrl from './select.png'

const WORLD_X_MAX = 200
const WORLD_Y_MAX = 200
const CELL_SIZE = 16
const DEFAULT_VIEWPORT_WIDTH = 896
const DEFAULT_VIEWPORT_HEIGHT = 608
const WORLD_WIDTH = WORLD_X_MAX * CELL_SIZE
const WORLD_HEIGHT = WORLD_Y_MAX * CELL_SIZE

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
let resizeObserver = null

function selectColor(color) {
	selectedColor.value = color
}

function toggleToolMenu() {
	isToolMenuOpen.value = !isToolMenuOpen.value
}

function clamp(value, min, max) {
	return Math.max(min, Math.min(max, value))
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

function clampCamera() {
	const { width, height } = getViewportDimensions()

	cameraX = Math.round(clamp(cameraX, 0, Math.max(0, WORLD_WIDTH - width)))
	cameraY = Math.round(clamp(cameraY, 0, Math.max(0, WORLD_HEIGHT - height)))
}

function getCanvas() {
	if (!(canvasRef.value instanceof HTMLCanvasElement)) {
		throw new Error('Canvas not found')
	}

	return canvasRef.value
}

function getViewportMousePos(event) {
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
	const mouseX = (event.clientX - rect.left - borderLeft) * scaleX
	const mouseY = (event.clientY - rect.top - borderTop) * scaleY

	return { mouseX, mouseY }
}

function getMousePos(event) {
	const { mouseX, mouseY } = getViewportMousePos(event)
	const worldX = mouseX + cameraX
	const worldY = mouseY + cameraY
	const cellX = clamp(Math.floor(worldX / CELL_SIZE), 0, WORLD_X_MAX - 1)
	const cellY = clamp(Math.floor(worldY / CELL_SIZE), 0, WORLD_Y_MAX - 1)

	pointerStatus.value = `Mouse pos (x,y): ${cellX},${cellY}`

	return { cellX, cellY }
}

function syncCanvasSize(centerCamera = false) {
	const canvas = getCanvas()
	const nextWidth = Math.max(1, Math.floor(canvas.clientWidth))
	const nextHeight = Math.max(1, Math.floor(canvas.clientHeight))

	if (canvas.width !== nextWidth || canvas.height !== nextHeight) {
		canvas.width = nextWidth
		canvas.height = nextHeight
	}

	if (centerCamera) {
		cameraX = (WORLD_WIDTH - canvas.width) / 2
		cameraY = (WORLD_HEIGHT - canvas.height) / 2
	}

	clampCamera()
}

function drawPixel(x, y, color) {
	ctx.fillStyle = color
	ctx.fillRect(x * CELL_SIZE - cameraX, y * CELL_SIZE - cameraY, CELL_SIZE, CELL_SIZE)
}

function drawPixels() {
	const { width, height } = getViewportDimensions()
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

	ctx.strokeStyle = '#A0A0A0'
	ctx.lineWidth = 1

	for (let x = 0; x <= WORLD_X_MAX; x += 1) {
		const screenX = x * CELL_SIZE - cameraX

		ctx.beginPath()
		ctx.moveTo(screenX + 0.5, 0)
		ctx.lineTo(screenX + 0.5, canvas.height)
		ctx.stroke()
	}

	for (let y = 0; y <= WORLD_Y_MAX; y += 1) {
		const screenY = y * CELL_SIZE - cameraY

		ctx.beginPath()
		ctx.moveTo(0, screenY + 0.5)
		ctx.lineTo(canvas.width, screenY + 0.5)
		ctx.stroke()
	}
}

function drawHover() {
	if (hoverCell === null || hoverImage === null || !hoverImage.complete) {
		return
	}

	ctx.drawImage(
		hoverImage,
		hoverCell.x * CELL_SIZE - cameraX,
		hoverCell.y * CELL_SIZE - cameraY,
		CELL_SIZE,
		CELL_SIZE,
	)
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

	placed++
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

function colorize(event) {
	const pos = getMousePos(event)

	recordPixelChange(pos.cellX, pos.cellY, selectedColor.value)
}

function beginPan(event) {
	event.preventDefault()
	isPanning = true
	isDrawing = false
	hoverCell = null
	commitStroke()

	const { mouseX, mouseY } = getViewportMousePos(event)

	lastPanX = mouseX
	lastPanY = mouseY
}

function panCamera(event) {
	const { mouseX, mouseY } = getViewportMousePos(event)
	const deltaX = mouseX - lastPanX
	const deltaY = mouseY - lastPanY

	cameraX -= deltaX
	cameraY -= deltaY
	clampCamera()

	lastPanX = mouseX
	lastPanY = mouseY
	pointerStatus.value = `Camera (x,y): ${Math.round(cameraX)},${Math.round(cameraY)}`
}

function handleMouseMove(event) {
	if (isPanning) {
		panCamera(event)
		return
	}

	const pos = getMousePos(event)

	hoverCell = {
		x: pos.cellX,
		y: pos.cellY,
	}

	if (isDrawing) {
		colorize(event)
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

	event.preventDefault()
	isDrawing = true
	beginStroke()

	const pos = getMousePos(event)

	hoverCell = {
		x: pos.cellX,
		y: pos.cellY,
	}

	colorize(event)
}

function handleMouseUp(event) {
	if (event.button === 1) {
		isPanning = false
		return
	}

	if (event.button !== 0) {
		return
	}

	isDrawing = false
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
	drawGrid()
	drawHover()
	pixelsLeft.value = (100 - placed) + "/100"

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
	isToolMenuOpen,
	pixelsLeft,
	pointerStatus,
	redo,
	selectColor,
	selectedColor,
	showGrid,
	toggleToolMenu,
	undo,
}
}
