<template>
	<main class="h-full bg-bg-main p-0 text-text-main sm:p-4">
		<section class="tplace-shell relative h-full min-h-0 overflow-hidden bg-bg-card sm:rounded-lg">
			<!-- START dev temporary pointer message -->
			<p class="pointer-status">{{ pointerStatus }}</p>
			<!-- END dev temporary pointer message -->

			<canvas
				ref="canvasRef"
				class="tplace-canvas block h-full w-full bg-bg-card"
				:class="isEyedropperMode ? 'cursor-copy' : (isPaintMode ? 'cursor-crosshair' : 'cursor-grab')"
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
				<div class="pointer-events-auto flex items-center gap-2">
					<button
						class="inline-flex min-h-12 max-w-[calc(100vw-1rem)] items-center justify-center gap-2 rounded-full border px-5 py-3 text-sm font-bold leading-tight text-white shadow-[0_12px_30px_rgba(37,99,235,0.45)] transition focus-visible:outline-2 focus-visible:outline-offset-2 active:scale-95 sm:min-w-56 sm:px-6 sm:text-lg"
						:class="[
							isLoginRequired
								? 'border-red-300 bg-red-600 shadow-[0_12px_30px_rgba(220,38,38,0.42)] hover:bg-red-500 focus-visible:outline-red-300'
								: 'border-white/35 bg-blue-600 hover:bg-blue-500 focus-visible:outline-blue-300',
							isPaintMode && canPaint && !isLoginRequired ? 'border-red-200 ring-4 ring-red-300/70' : '',
						]"
						type="button"
						:title="paintButtonTitle"
						aria-controls="tplace-tools"
						:aria-expanded="!isLoginRequired && isPaintMode && isToolMenuOpen"
						@click="handlePaintButtonClick"
					>
						<FontAwesomeIcon
							:icon="byPrefixAndName.fas[isLoginRequired ? 'right-to-bracket' : (isPaintMode ? 'check' : 'paintbrush')]"
							class="text-sm sm:text-base"
						/>
						<span class="text-center">{{ paintButtonText }}</span>
						<span
							v-if="!isLoginRequired && !isPaintMode"
							class="rounded-full bg-white/15 px-2 py-0.5 text-sm font-bold tabular-nums text-white/90"
						>{{ regenerationSecondsLeft }}s</span>
					</button>

					<button
						v-if="!isLoginRequired && isPaintMode && !isToolMenuOpen"
						class="grid size-12 place-items-center rounded-full border border-white/35 bg-blue-600 text-white shadow-[0_12px_30px_rgba(37,99,235,0.35)] transition hover:bg-blue-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-300 active:scale-95"
						type="button"
						title="Expand paint tools (X)"
						aria-label="Expand paint tools"
						aria-controls="tplace-tools"
						:aria-expanded="isToolMenuOpen"
						@click="toggleToolMenu"
					>
						<FontAwesomeIcon :icon="byPrefixAndName.fas['chevron-down']" />
					</button>
				</div>

				<div
					id="tplace-tools"
					class="pointer-events-auto flex w-full max-w-3xl flex-col items-center gap-2 transition duration-200 ease-out"
					:class="isPaintMode ? 'translate-y-0 opacity-100' : 'pointer-events-none -translate-y-4 opacity-0'"
					:aria-hidden="!isPaintMode"
				>
					<div
						class="w-full origin-top overflow-hidden rounded-2xl border border-borders-outline/80 bg-bg-card/95 shadow-[0_16px_40px_rgba(20,20,20,0.22)] backdrop-blur-md transition duration-200 ease-out"
						:class="isToolMenuOpen ? 'max-h-96 scale-100 p-2 opacity-100 sm:p-3' : 'pointer-events-none max-h-0 scale-95 border-transparent p-0 opacity-0'"
					>
						<div class="mb-2 flex flex-wrap items-center justify-between gap-2">
							<div class="flex min-w-0 items-center gap-2">
								<span
									class="grid size-8 shrink-0 place-items-center rounded-xl bg-button-1-normal text-text-button-1 shadow-[0_8px_18px_rgba(0,0,0,0.18)]"
									aria-hidden="true"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['paintbrush']" />
								</span>
								<div class="min-w-0">
									<p class="truncate text-sm font-bold leading-tight text-text-main">Paint pixel</p>
									<div class="mt-1 flex min-w-0 flex-wrap items-center gap-1.5 text-xs font-semibold leading-tight text-text-main/65">
										<span class="whitespace-nowrap">{{ pixelsLeft }} charges</span>
										<button
											class="grid size-6 place-items-center rounded-lg border border-borders-outline bg-bg-main text-[10px] text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover active:scale-95"
											type="button"
											title="Upgrade max charges"
											aria-label="Upgrade max charges"
											@click="openUpgradeModal('max-pixels')"
										>
											<FontAwesomeIcon :icon="byPrefixAndName.fas['arrow-up']" />
										</button>
										<span class="whitespace-nowrap">{{ cooldownLabel }}</span>
										<button
											class="grid size-6 place-items-center rounded-lg border border-borders-outline bg-bg-main text-[10px] text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover active:scale-95 disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:bg-bg-main"
											type="button"
											:title="canUpgradeCooldown ? 'Upgrade regeneration cooldown' : 'Minimum cooldown reached'"
											aria-label="Upgrade regeneration cooldown"
											:disabled="!canUpgradeCooldown"
											@click="openUpgradeModal('cooldown')"
										>
											<FontAwesomeIcon :icon="byPrefixAndName.fas['bolt']" />
										</button>
									</div>
								</div>
							</div>

							<div class="flex shrink-0 flex-wrap items-center justify-end gap-1.5">
								<div
									class="inline-flex h-9 shrink-0 items-center gap-1.5 rounded-xl border border-borders-outline bg-bg-main px-2 text-sm font-bold tabular-nums text-text-main shadow-sm"
									aria-label="Nyancoins"
									:title="`${nyancoins} Nyancoins`"
								>
									<img :src="nyancoinIcon" alt="" class="size-5 shrink-0" draggable="false">
									<span>{{ nyancoins }}</span>
								</div>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									:class="isEyedropperMode ? 'border-button-1-hover bg-button-1-normal text-text-button-1 ring-2 ring-button-1-hover/70 hover:bg-button-1-hover' : ''"
									type="button"
									title="Pick canvas color (F)"
									aria-label="Pick canvas color"
									:aria-pressed="isEyedropperMode"
									@click="toggleEyedropperMode"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['eye-dropper']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									:class="isEraserMode ? 'border-button-1-hover bg-button-1-normal text-text-button-1 ring-2 ring-button-1-hover/70 hover:bg-button-1-hover' : ''"
									type="button"
									title="Erase draft pixels (E)"
									aria-label="Erase draft pixels"
									:aria-pressed="isEraserMode"
									@click="toggleEraserMode"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['eraser']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Undo (Ctrl+Z)"
									aria-label="Undo"
									@click="undo"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['arrow-rotate-left']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Redo (Ctrl+Shift+Z)"
									aria-label="Redo"
									@click="redo"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['arrow-rotate-right']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-borders-outline bg-bg-main text-sm text-text-main shadow-sm transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
									type="button"
									title="Collapse paint tools (X)"
									aria-label="Collapse paint tools"
									:aria-expanded="isToolMenuOpen"
									aria-controls="tplace-tools"
									@click="toggleToolMenu"
								>
									<FontAwesomeIcon :icon="byPrefixAndName.fas['chevron-up']" />
								</button>
								<button
									class="grid size-9 place-items-center rounded-xl border border-red-400/60 bg-bg-main text-sm text-red-500 shadow-sm transition hover:bg-red-500 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-400"
									type="button"
									title="Cancel paint draft (Esc)"
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
									ref="colorPaletteRef"
									class="tplace-scrollbar grid max-w-full cursor-grab grid-flow-col grid-rows-2 gap-1.5 overflow-x-auto rounded-2xl bg-bg-main/80 p-2 shadow-inner select-none sm:grid-rows-1"
									:class="isPaletteDragging ? 'cursor-grabbing' : ''"
									aria-label="Color palette"
									@wheel.prevent
									@pointerdown="handlePalettePointerDown"
									@pointermove="handlePalettePointerMove"
									@pointerup="handlePalettePointerEnd"
									@pointercancel="handlePalettePointerEnd"
									@lostpointercapture="handlePalettePointerEnd"
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
										:title="`${color.name} (Q)`"
										:aria-label="color.name"
										:aria-pressed="selectedColor === color.value"
										@click="handleColorClick(color.value, $event)"
									/>
								</div>
							</div>

							<label class="inline-flex shrink-0 cursor-pointer select-none items-center justify-between gap-3 rounded-2xl border border-borders-outline bg-bg-main/80 px-3 py-2 text-sm font-bold text-text-main shadow-sm sm:min-w-36" title="Toggle grid (G)">
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
			</div>
			<div
				v-if="upgradeModalType !== null"
				class="absolute inset-0 z-20 grid place-items-center bg-black/45 p-4"
				@click.self="closeUpgradeModal"
			>
				<section class="w-full max-w-sm rounded-2xl border border-borders-outline bg-bg-card p-4 text-text-main shadow-[0_24px_70px_rgba(0,0,0,0.35)] sm:p-5">
					<div class="flex items-start gap-3">
						<span class="grid size-10 shrink-0 place-items-center rounded-xl bg-button-1-normal text-text-button-1">
							<FontAwesomeIcon :icon="isCooldownUpgrade ? byPrefixAndName.fas['bolt'] : byPrefixAndName.fas['arrow-up']" />
						</span>
						<div class="min-w-0 flex-1">
							<h2 class="text-base font-bold leading-tight">{{ upgradeModalTitle }}</h2>
							<p class="mt-1 text-sm font-semibold leading-snug text-text-main/65">{{ upgradeModalDescription }}</p>
						</div>
						<button
							class="grid size-8 shrink-0 place-items-center rounded-xl text-text-main/70 transition hover:bg-button-2-normal hover:text-text-main focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
							type="button"
							title="Close"
							aria-label="Close upgrade modal"
							@click="closeUpgradeModal"
						>
							<FontAwesomeIcon :icon="byPrefixAndName.fas['xmark']" />
						</button>
					</div>

					<div class="mt-4 grid grid-cols-2 gap-2 text-sm font-semibold">
						<div class="rounded-xl bg-bg-main/80 p-3">
							<p class="text-xs uppercase text-text-main/55">Nyancoins</p>
							<p class="mt-1 text-lg font-bold tabular-nums">{{ nyancoins }}</p>
						</div>
						<div class="rounded-xl bg-bg-main/80 p-3">
							<p class="text-xs uppercase text-text-main/55">Cost</p>
							<p class="mt-1 text-lg font-bold tabular-nums">{{ upgradeCost }}</p>
						</div>
					</div>

					<label class="mt-4 block text-sm font-bold text-text-main" for="tplace-upgrade-quantity">Quantity</label>
					<div class="mt-2 flex items-center gap-2">
						<button
							class="grid size-10 place-items-center rounded-xl border border-borders-outline bg-bg-main text-text-main transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover active:scale-95"
							type="button"
							title="Decrease quantity"
							aria-label="Decrease quantity"
							@click="adjustUpgradeQuantity(-1)"
						>
							<FontAwesomeIcon :icon="byPrefixAndName.fas['minus']" />
						</button>
						<input
							id="tplace-upgrade-quantity"
							v-model.number="upgradeQuantity"
							class="h-10 min-w-0 flex-1 rounded-xl border border-borders-outline bg-bg-main px-3 text-center text-base font-bold tabular-nums text-text-main focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
							type="number"
							:min="1"
							:max="upgradeQuantityMax"
							@change="upgradeQuantity = normalizeUpgradeQuantity(upgradeQuantity)"
						>
						<button
							class="grid size-10 place-items-center rounded-xl border border-borders-outline bg-bg-main text-text-main transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover active:scale-95"
							type="button"
							title="Increase quantity"
							aria-label="Increase quantity"
							@click="adjustUpgradeQuantity(1)"
						>
							<FontAwesomeIcon :icon="byPrefixAndName.fas['plus']" />
						</button>
					</div>

					<p class="mt-3 text-sm font-semibold text-text-main/70">{{ upgradePreview }}</p>
					<p v-if="upgradeError || !canAffordUpgrade" class="mt-3 rounded-xl border border-red-400/60 bg-red-500/10 px-3 py-2 text-sm font-bold text-red-500">{{ upgradeError || 'Not enough nyancoins' }}</p>

					<div class="mt-5 flex justify-end gap-2">
						<button
							class="rounded-xl border border-borders-outline bg-bg-main px-4 py-2 text-sm font-bold text-text-main transition hover:bg-button-2-normal focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover"
							type="button"
							@click="closeUpgradeModal"
						>Cancel</button>
						<button
							class="rounded-xl bg-button-1-normal px-4 py-2 text-sm font-bold text-text-button-1 transition hover:bg-button-1-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-button-1-hover disabled:cursor-not-allowed disabled:opacity-45"
							type="button"
							:disabled="!canConfirmUpgrade"
							@click="confirmUpgradePurchase"
						>{{ isBuyingUpgrade ? 'Buying...' : 'Buy upgrade' }}</button>
					</div>
				</section>
			</div>
		</section>
	</main>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useThemeStore } from '@storage'
import nyancoinIcon from '@assets/nyancoin.png'
import tplaceNavbarLogoLight from '@assets/ft_cat_pixel_title.png'
import tplaceNavbarLogoDark from '@assets/ft_cat_pixel_title_dark.png'
import { runTplace } from './tplace.js'
import './TPlace.css'

const {
	cancelPaintMode,
	canPaint,
	canvasRef,
	buyMaxPixelUpgrades,
	buyRegenerationDelayUpgrades,
	colors,
	confirmDraftPixels,
	draftPixelCount,
	getCooldownUpgradeCost,
	getMaxPixelUpgradeCost,
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
	MIN_REGENERATION_DELAY_SECONDS,
	nyancoins,
	pixelsLeft,
	pointerStatus,
	redo,
	regenerationDelaySeconds,
	regenerationSecondsLeft,
	selectColor,
	selectedColor,
	showGrid,
	toggleEraserMode,
	toggleEyedropperMode,
	togglePaintMode,
	toggleToolMenu,
	undo,
} = runTplace()

const theme = useThemeStore()
const tplaceNavbarLogo = computed(() => theme.getThemeIndex() === 0 ? tplaceNavbarLogoLight : tplaceNavbarLogoDark)
let navbarLogoImage = null
let originalNavbarLogo = null
let navbarLogoFrameId = 0
let stopNavbarLogoWatcher = null

const colorPaletteRef = ref(null)
const isPaletteDragging = ref(false)
const paletteDragState = {
	pointerId: null,
	startX: 0,
	startScrollLeft: 0,
	didDrag: false,
	suppressClick: false,
}

function getNavbarLogoImage() {
	return document.querySelector('nav a[aria-label="back to home"] img')
}

function restoreNavbarLogo() {
	if (!(navbarLogoImage instanceof HTMLImageElement) || originalNavbarLogo === null) {
		return
	}

	navbarLogoImage.src = originalNavbarLogo.src
	navbarLogoImage.alt = originalNavbarLogo.alt

	if (originalNavbarLogo.srcset === null) {
		navbarLogoImage.removeAttribute('srcset')
	} else {
		navbarLogoImage.setAttribute('srcset', originalNavbarLogo.srcset)
	}

	navbarLogoImage = null
	originalNavbarLogo = null
}

function applyTplaceNavbarLogo() {
	const image = getNavbarLogoImage()

	if (!(image instanceof HTMLImageElement)) {
		return
	}

	if (navbarLogoImage !== image) {
		restoreNavbarLogo()
		navbarLogoImage = image
		originalNavbarLogo = {
			src: image.src,
			srcset: image.getAttribute('srcset'),
			alt: image.alt,
		}
	}

	image.src = tplaceNavbarLogo.value
	image.alt = 'TPlace'
	image.removeAttribute('srcset')
}

function scheduleTplaceNavbarLogo() {
	if (navbarLogoFrameId !== 0) {
		window.cancelAnimationFrame(navbarLogoFrameId)
	}

	navbarLogoFrameId = window.requestAnimationFrame(() => {
		navbarLogoFrameId = 0
		applyTplaceNavbarLogo()
	})
}

const paintButtonText = computed(() => {
	if (isLoginRequired.value) {
		return 'Log In to place your pixels !'
	}

	if (isPaintMode.value) {
		return `Place ${draftPixelCount.value} pixels`
	}

	return `Paint ${pixelsLeft.value}`
})

const paintButtonTitle = computed(() => {
	if (isLoginRequired.value) {
		return 'Log in to place your pixels'
	}

	if (isPaintMode.value) {
		return 'Place pixels (Enter)'
	}

	return 'Open paint tools'
})

function getPaletteElement(event) {
	return event.currentTarget instanceof HTMLElement ? event.currentTarget : colorPaletteRef.value
}

function handlePalettePointerDown(event) {
	const palette = getPaletteElement(event)

	if (!(palette instanceof HTMLElement) || event.button !== 0 || event.pointerType !== 'mouse') {
		return
	}

	paletteDragState.pointerId = event.pointerId
	paletteDragState.startX = event.clientX
	paletteDragState.startScrollLeft = palette.scrollLeft
	paletteDragState.didDrag = false
	isPaletteDragging.value = false
}

function handlePalettePointerMove(event) {
	const palette = getPaletteElement(event)

	if (!(palette instanceof HTMLElement) || paletteDragState.pointerId !== event.pointerId) {
		return
	}

	const deltaX = event.clientX - paletteDragState.startX

	if (!paletteDragState.didDrag && Math.abs(deltaX) > 8) {
		paletteDragState.didDrag = true
		paletteDragState.suppressClick = true
		isPaletteDragging.value = true
		palette.setPointerCapture?.(event.pointerId)
	}

	if (!paletteDragState.didDrag) {
		return
	}

	event.preventDefault()
	palette.scrollLeft = paletteDragState.startScrollLeft - deltaX
}

function handlePalettePointerEnd(event) {
	const palette = getPaletteElement(event)

	if (palette instanceof HTMLElement && paletteDragState.pointerId === event.pointerId) {
		try {
			palette.releasePointerCapture?.(event.pointerId)
		} catch {
		}
	}

	paletteDragState.pointerId = null
	isPaletteDragging.value = false
	window.setTimeout(() => {
		paletteDragState.didDrag = false
		paletteDragState.suppressClick = false
	}, 0)
}

function handleColorClick(color, event) {
	if (paletteDragState.suppressClick) {
		event.preventDefault()
		paletteDragState.suppressClick = false
		return
	}

	selectColor(color)
}

onMounted(() => {
	scheduleTplaceNavbarLogo()
	stopNavbarLogoWatcher = watch(tplaceNavbarLogo, scheduleTplaceNavbarLogo, { flush: 'post' })
})

onBeforeUnmount(() => {
	if (navbarLogoFrameId !== 0) {
		window.cancelAnimationFrame(navbarLogoFrameId)
		navbarLogoFrameId = 0
	}

	stopNavbarLogoWatcher?.()
	stopNavbarLogoWatcher = null
	restoreNavbarLogo()
})

const upgradeModalType = ref(null)
const upgradeQuantity = ref(1)
const upgradeError = ref('')
const isBuyingUpgrade = ref(false)

const canUpgradeCooldown = computed(() => regenerationDelaySeconds.value > MIN_REGENERATION_DELAY_SECONDS)
const cooldownLabel = computed(() => 'Next in ' + regenerationSecondsLeft.value + ' sec (' + regenerationDelaySeconds.value + ' seconds)')
const isCooldownUpgrade = computed(() => upgradeModalType.value === 'cooldown')
const upgradeQuantityMax = computed(() => (isCooldownUpgrade.value
	? Math.max(1, regenerationDelaySeconds.value - MIN_REGENERATION_DELAY_SECONDS)
	: 999))
const upgradeCost = computed(() => (isCooldownUpgrade.value
	? getCooldownUpgradeCost(normalizeUpgradeQuantity(upgradeQuantity.value))
	: getMaxPixelUpgradeCost(normalizeUpgradeQuantity(upgradeQuantity.value))))
const canAffordUpgrade = computed(() => nyancoins.value >= upgradeCost.value)
const canConfirmUpgrade = computed(() => (
	!isBuyingUpgrade.value
	&& upgradeModalType.value !== null
	&& upgradeCost.value > 0
	&& canAffordUpgrade.value
	&& (!isCooldownUpgrade.value || canUpgradeCooldown.value)
))
const upgradeModalTitle = computed(() => (isCooldownUpgrade.value
	? 'Upgrade regeneration cooldown'
	: 'Upgrade max charges'))
const upgradeModalDescription = computed(() => (isCooldownUpgrade.value
	? 'Reduce the regeneration delay by 1 second per upgrade.'
	: 'Increase your maximum saved pixel charges.'))
const upgradePreview = computed(() => {
	const quantity = normalizeUpgradeQuantity(upgradeQuantity.value)

	if (isCooldownUpgrade.value) {
		const nextDelay = Math.max(MIN_REGENERATION_DELAY_SECONDS, regenerationDelaySeconds.value - quantity)
		return 'Cooldown: ' + regenerationDelaySeconds.value + ' seconds -> ' + nextDelay + ' seconds'
	}

	return 'Max charges: +' + quantity
})

function normalizeUpgradeQuantity(value) {
	const amount = Number(value)

	if (!Number.isInteger(amount) || amount < 1) {
		return 1
	}

	return Math.min(amount, upgradeQuantityMax.value)
}

function openUpgradeModal(type) {
	if (type === 'cooldown' && !canUpgradeCooldown.value) {
		return
	}

	upgradeModalType.value = type
	upgradeQuantity.value = 1
	upgradeError.value = ''
}

function closeUpgradeModal() {
	if (isBuyingUpgrade.value) {
		return
	}

	upgradeModalType.value = null
	upgradeError.value = ''
}

function adjustUpgradeQuantity(delta) {
	upgradeQuantity.value = normalizeUpgradeQuantity(upgradeQuantity.value + delta)
	upgradeError.value = ''
}

async function confirmUpgradePurchase() {
	if (!canConfirmUpgrade.value) {
		upgradeError.value = nyancoins.value < upgradeCost.value ? 'Not enough nyancoins' : ''
		return
	}

	isBuyingUpgrade.value = true
	upgradeError.value = ''

	try {
		const quantity = normalizeUpgradeQuantity(upgradeQuantity.value)

		if (isCooldownUpgrade.value) {
			await buyRegenerationDelayUpgrades(quantity)
		} else {
			await buyMaxPixelUpgrades(quantity)
		}

		upgradeModalType.value = null
	} catch (error) {
		console.log(error)
		upgradeError.value = error.message || 'Upgrade purchase failed'
	} finally {
		isBuyingUpgrade.value = false
	}
}

async function handlePaintButtonClick() {
	if (isLoginRequired.value) {
		window.location.href = loginUrl.value
		return
	}

	if (!isPaintMode.value) {
		togglePaintMode()
		return
	}

	await confirmDraftPixels()
}
</script>
