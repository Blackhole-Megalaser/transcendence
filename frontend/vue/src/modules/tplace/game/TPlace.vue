<template>
	<main class="h-full bg-bg-main p-0 text-text-main sm:p-4">
		<section class="tplace-shell relative h-full min-h-0 overflow-hidden bg-bg-card sm:rounded-lg">
			<!-- START dev temporary pointer message -->
			<p class="pointer-status">{{ pointerStatus }}</p>
			<!-- END dev temporary pointer message -->

			<canvas
				ref="canvasRef"
				class="tplace-canvas block h-full w-full bg-bg-card"
				:class="isPaintMode ? 'cursor-crosshair' : 'cursor-grab'"
				width="896"
				height="608"
				@mousemove="handleMouseMove"
				@mouseleave="handleMouseLeave"
				@mousedown="handleMouseDown"
				@mouseup="handleMouseUp"
				@touchstart.prevent="handleTouchStart"
				@touchmove.prevent="handleTouchMove"
				@touchend.prevent="handleTouchEnd"
				@touchcancel.prevent="handleTouchCancel"
				@wheel.prevent="handleWheel"
			/>

			<div class="pointer-events-none absolute inset-x-2 bottom-2 z-10 flex flex-col items-center gap-2 sm:inset-x-4 sm:bottom-4">
				<div
					id="tplace-tools"
					class="pointer-events-auto flex w-full max-w-3xl flex-col items-center gap-2 transition duration-200 ease-out"
					:class="isPaintMode ? 'translate-y-0 opacity-100' : 'pointer-events-none translate-y-4 opacity-0'"
					:aria-hidden="!isPaintMode"
				>
					<div
						class="w-full origin-bottom overflow-hidden rounded-2xl border border-borders-outline/80 bg-bg-card/95 shadow-[0_16px_40px_rgba(20,20,20,0.22)] backdrop-blur-md transition duration-200 ease-out"
						:class="isToolMenuOpen ? 'max-h-96 scale-100 p-2 opacity-100 sm:p-3' : 'pointer-events-none max-h-0 scale-95 border-transparent p-0 opacity-0'"
					>
						<div class="mb-2 flex items-center justify-between gap-2">
							<div class="flex min-w-0 items-center gap-2">
								<span
									class="grid size-8 shrink-0 place-items-center rounded-xl bg-button-1-normal text-text-button-1 shadow-[0_8px_18px_rgba(0,0,0,0.18)]"
									aria-hidden="true"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['paintbrush']" />
								</span>
								<div class="min-w-0">
									<p class="truncate text-sm font-bold leading-tight text-text-main">Paint pixel</p>
									<p class="truncate text-xs font-semibold leading-tight text-text-main/65">{{ pixelsLeft }} charges</p>
								</div>
							</div>

							<div class="flex shrink-0 items-center gap-1.5">
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									:class="isEraserMode ? 'border-button-1-hover bg-button-1-normal text-text-button-1 ring-2 ring-button-1-hover/70 hover:bg-button-1-hover' : ''"
									type="button"
									title="Gommer les pixels temporaires"
									aria-label="Erase draft pixels"
									:aria-pressed="isEraserMode"
									@click="toggleEraserMode"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['eraser']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Annuler"
									aria-label="Undo"
									@click="undo"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['arrow-rotate-left']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Refaire"
									aria-label="Redo"
									@click="redo"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['arrow-rotate-right']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Reduire"
									aria-label="Collapse paint tools"
									:aria-expanded="isToolMenuOpen"
									aria-controls="tplace-tools"
									@click="toggleToolMenu"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['chevron-down']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-red-400/60 bg-bg-main text-sm text-red-500 shadow-sm transition hover:bg-red-500 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-400"
									type="button"
									title="Annuler le dessin"
									aria-label="Cancel paint draft"
									@click="cancelPaintMode"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['xmark']" />
								</button>
							</div>
						</div>

						<div class="flex flex-col gap-2 sm:flex-row sm:items-end">
							<div class="min-w-0 flex-1">
								<div
									class="tplace-scrollbar grid max-w-full grid-flow-col grid-rows-2 gap-1.5 overflow-x-auto rounded-2xl bg-bg-main/80 p-2 shadow-inner sm:grid-rows-1"
									aria-label="Color palette"
								>
									<button
										v-for="color in colors"
										:key="color.value"
										class="relative size-8 rounded-xl border-2 border-bg-card shadow-[0_0_0_1px_rgba(0,0,0,0.22)] transition hover:scale-105 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
										:class="!isEraserMode && selectedColor === color.value
											? 'z-10 scale-105 ring-2 ring-button-1-hover ring-offset-2 ring-offset-bg-card'
											: ''"
										type="button"
										:style="{ backgroundColor: color.value }"
										:title="color.name"
										:aria-label="color.name"
										:aria-pressed="selectedColor === color.value"
										@click="selectColor(color.value)"
									/>
								</div>
							</div>

							<label class="inline-flex shrink-0 cursor-pointer select-none items-center justify-between gap-3 rounded-2xl border border-borders-outline bg-bg-main/80 px-3 py-2 text-sm font-bold text-text-main shadow-sm sm:min-w-36">
								<span class="flex items-center gap-2">
									<FontAwesomeIcon :icon="byPrefixAndName.fas['table-cells']" class="text-xs opacity-75" />
									Grid
								</span>
								<input v-model="showGrid" class="peer sr-only" type="checkbox" :aria-label="gridLabel">
								<span class="relative h-6 w-11 rounded-full bg-button-2-normal transition peer-checked:bg-button-1-hover peer-checked:[&>span]:translate-x-5">
									<span class="absolute left-1 top-1 size-4 rounded-full bg-bg-card shadow transition"></span>
								</span>
							</label>
						</div>
					</div>
				</div>

				<div class="pointer-events-auto flex items-center gap-2">
					<button
						class="inline-flex min-h-12 min-w-44 items-center justify-center gap-2 rounded-full border border-white/35 bg-blue-600 px-6 py-3 text-base font-bold text-white shadow-[0_12px_30px_rgba(37,99,235,0.45)] transition hover:bg-blue-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-300 active:scale-95 sm:min-w-56 sm:text-lg"
						:class="isPaintMode && canPaint ? 'border-red-200 ring-4 ring-red-300/70' : ''"
						type="button"
						aria-controls="tplace-tools"
						:aria-expanded="isPaintMode && isToolMenuOpen"
						@click="handlePaintButtonClick"
					>
						<FontAwesomeIcon :icon="byPrefixAndName.fas['paintbrush']" class="text-sm sm:text-base" />
						<span>Paint {{ pixelsLeft }}</span>
						<span class="rounded-full bg-white/15 px-2 py-0.5 text-sm font-bold tabular-nums text-white/90">{{ regenerationSecondsLeft }}s</span>
					</button>

					<button
						v-if="isPaintMode && !isToolMenuOpen"
						class="grid size-12 place-items-center rounded-full border border-white/35 bg-blue-600 text-white shadow-[0_12px_30px_rgba(37,99,235,0.35)] transition hover:bg-blue-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-300 active:scale-95"
						type="button"
						title="Ouvrir les outils"
						aria-label="Expand paint tools"
						aria-controls="tplace-tools"
						:aria-expanded="isToolMenuOpen"
						@click="toggleToolMenu"
					>
						<FontAwesomeIcon :icon="byPrefixAndName.fas['chevron-up']" />
					</button>
				</div>
			</div>
		</section>
	</main>
</template>

<script setup>
import { runTplace } from './tplace.js'
import './TPlace.css'

const {
	cancelPaintMode,
	canPaint,
	canvasRef,
	colors,
	confirmDraftPixels,
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
	isPaintMode,
	isToolMenuOpen,
	pixelsLeft,
	pointerStatus,
	redo,
	regenerationSecondsLeft,
	selectColor,
	selectedColor,
	showGrid,
	toggleEraserMode,
	togglePaintMode,
	toggleToolMenu,
	undo,
} = runTplace()

async function handlePaintButtonClick() {
	if (!isPaintMode.value) {
		togglePaintMode()
		return
	}

	await confirmDraftPixels()
}
</script>
