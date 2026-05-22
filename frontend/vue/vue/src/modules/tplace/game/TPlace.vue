<template>
	<main class="h-full bg-bg-main p-2 sm:p-4 text-text-main">
		<section class="tplace-shell relative h-full min-h-0 overflow-hidden rounded-lg">
			<!-- START dev temporary pointer message -->
			<p class="pointer-status">{{ pointerStatus }}</p>
			<!-- END dev temporary pointer message -->

			<div class="canvas-overlay overlay-right">
				<div class="history-controls" aria-label="History controls">
					<button class="history-button" type="button" title="Annuler" aria-label="Undo" @click="undo">
						↩
					</button>
					<button class="history-button" type="button" title="Refaire" aria-label="Redo" @click="redo">
						↪
					</button>
				</div>

				<div class="color-palette" aria-label="Color palette">
					<button
						v-for="color in colors"
						:key="color.value"
						class="color-swatch"
						:class="{ 'is-selected': selectedColor === color.value }"
						type="button"
						:style="{ '--swatch-color': color.value }"
						:title="color.name"
						:aria-label="color.name"
						@click="selectColor(color.value)"
					/>
				</div>

				<label class="grid-toggle">
					<input v-model="showGrid" type="checkbox">
					<span class="grid-toggle-track">
						<span class="grid-toggle-thumb"></span>
					</span>
					<span class="grid-toggle-label">{{ gridLabel }}</span>
				</label>
			</div>

			<div class="canvas-overlay overlay-bottom">
				<button class="pretty-button" type="button">
					Paint {{ pixelsLeft }}
					<span
						v-for="star in 6"
						:key="star"
						:class="['star', `star-${star}`]"
						aria-hidden="true"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							xml:space="preserve"
							version="1.1"
							viewBox="0 0 784.11 815.53"
						>
							<path
								class="fil0"
								d="M392.05 0c-20.9,210.08 -184.06,378.41 -392.05,407.78 207.96,29.37 371.12,197.68 392.05,407.74 20.93,-210.06 184.09,-378.37 392.05,-407.74 -207.98,-29.38 -371.16,-197.69 -392.06,-407.78z"
							/>
						</svg>
					</span>
				</button>
			</div>

			<canvas
				ref="canvasRef"
				class="block h-full w-full cursor-crosshair bg-bg-card"
				width="896"
				height="608"
				@mousemove="handleMouseMove"
				@mouseleave="handleMouseLeave"
				@mousedown="handleMouseDown"
				@mouseup="handleMouseUp"
			/>
		</section>
	</main>
</template>

<script setup>
import { runTplace } from './tplace.js'
import './TPlace.css'

const {
	canvasRef,
	colors,
	gridLabel,
	handleMouseDown,
	handleMouseLeave,
	handleMouseMove,
	handleMouseUp,
	pixelsLeft,
	pointerStatus,
	redo,
	selectColor,
	selectedColor,
	showGrid,
	undo,
} = runTplace()
</script>
