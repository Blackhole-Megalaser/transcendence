<script setup>
	import { ref, onMounted } from 'vue';

	const width = 1000;
	const height = 600;
	const canvasRef = ref(null);
	const vueCanvas = ref(null);
	const isDrawing = ref(false);
	const coord = ref({x: 0, y: 0});
	const penColor = ref('#000000');

	onMounted(() => {
		vueCanvas.value = canvasRef.value.getContext("2d");
	});

	const reposition = (event) => {
		coord.value.x = event.offsetX;
		coord.value.y = event.offsetY;
	};
	
	const start = (event) => {
		isDrawing.value = true;
		reposition(event);
	};

	const stop = () => {
		isDrawing.value = false;
	};

	const clear = () => {
		vueCanvas.value.clearRect(0, 0, 1000, 600);
	};

	const draw = (event) => {
		if (!isDrawing.value) return;

		const ctx = vueCanvas.value;

		ctx.beginPath();
		ctx.lineWidth = 4;
		ctx.lineCap = 'round';
		ctx.strokeStyle = penColor.value;

		ctx.moveTo(coord.value.x, coord.value.y);
		reposition(event);
		ctx.lineTo(coord.value.x, coord.value.y);
		ctx.stroke();
	};

	const penColorBlue = () => {
		penColor = '#0000FF';
	};
</script>

<template>
	<div class="flex justify-center bg-white border-4 border-solid border-blue-500">
		<div class="w-1/4 mr-10 border-4 border-solid border-red-500">
			<div class="bg-white border-4 border-solid border-green-500">
				
			</div>
		</div>
		<canvas ref="canvasRef" :width="width" :height="height"
			class="border-4 border-solid border-red-500 bg-white"
			@mousedown="start"
			@mousemove="draw"
			@mouseup="stop"
			@mouseleave="stop">
		</canvas>
		<div class="w-1/4 ml-10 border-4 border-solid border-red-500">
			<div class="bg-white border-4 border-solid border-green-500">

			</div>
		</div>
	</div>
	<div class="flex justify-center">
		<div class="grid grid-flow-col grid-rows-1 bg-pink-pastel-100 border-4 border-solid rounded-lg border-pink-pastel-300">
			<button class="bg-[var(--color-sidebar)]">
				<svg class="stroke-[0.5] size-50"
						xlms="http://www.w3.org/2000/svg"
						viewBox="0 0 32 32"
						stroke-width="2" stroke-miterlimit="10">
					<ellipse class="stroke-[0.7] stroke-[#917F97] fill-pink-50" cx="16" cy="18" rx="13" ry="15"/>
					<ellipse class="hover:stroke-blue-500 hover:fill-blue-400 stroke-blue-600 fill-blue-500" @click="penColor = 'blue'" cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-red-500 hover:fill-red-400 stroke-red-600 fill-red-500" @click="penColor = 'red'" cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-green-500 hover:fill-green-400 stroke-green-600 fill-green-500" @click="penColor = 'green'" cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-yellow-500 hover:fill-yellow-400 stroke-yellow-600 fill-yellow-500" @click="penColor = 'yellow'" cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
					<path class="hover:stroke-gray-800 hover:fill-gray-900 stroke-gray-800 fill-black" @click="penColor = 'black'" d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
						s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
						C23,21.207,19.966,20.966,19,20z"/>
					<rect class="stroke-[#917F97] fill-pink-50" x="5.5" y="27" width="21" height="32"></rect>
					<rect class="fill-pink-50" x="5.75" y="26.5" width="20.5" height="32"></rect>
				</svg>
			</button>
			<button class="bg-[var(--color-sidebar)]">
				<svg class="stroke-[0.5] size-50"
						xlms="http://www.w3.org/2000/svg"
						viewBox="0 0 32 32"
						stroke-width="2" stroke-miterlimit="10">
					<ellipse class="stroke-[0.7] stroke-[#917F97] fill-pink-50" cx="16" cy="18" rx="13" ry="15"/>
					<ellipse class="hover:stroke-pink-500 hover:fill-pink-400 stroke-pink-600 fill-pink-500" @click="penColor = 'pink'" cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-violet-500 hover:fill-violet-400 stroke-violet-600 fill-violet-500" @click="penColor = 'violet'" cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-yellow-800 hover:fill-yellow-700 stroke-yellow-900 fill-yellow-800" @click="penColor = 'brown'" cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
					<ellipse class="hover:stroke-gray-500 hover:fill-gray-400 stroke-gray-600 fill-gray-500" @click="penColor = 'gray'" cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
					<path class="hover:stroke-gray-200 hover:fill-gray-50 stroke-gray-200 fill-white" @click="penColor = 'white'" d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
						s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
						C23,21.207,19.966,20.966,19,20z"/>
					<rect class="stroke-[#917F97] fill-pink-50" x="5.5" y="27" width="21" height="32"></rect>	
					<rect class="fill-pink-50" x="5.75" y="26.5" width="20.5" height="32"></rect>
				</svg>
			</button>
			<button class="bg-[var(--color-sidebar)] hover:bg-lavender-pastel-50" @click="clear">
				<svg 
					class="size-50 fill-current" 
					viewBox="0 0 512 512" 
					xmlns="http://www.w3.org/2000/svg">
					<g>
						<path d="m296 95.999v40c-26.667 6.667-53.333 6.667-80 0v-40c25.433-8.82 52.204-8.069 80 0z" fill="#fdcb02"></path>
						<path d="m296 65.999v30h-80v-30c0-22.09 17.91-40 40-40 22.08 0 40 17.919 40 40z" fill="#737a7e"></path>
						<path d="m296 135.999v70c-26.516 11.082-53.193 10.251-80 0v-70z" fill="#737a7e"></path>
						<path d="m116 205.999 38 120-98 160z" fill="#989dec"></path>
						<path d="m396 205.999 60 280-95-160z" fill="#989dec"></path>
						<path d="m116 205.999 20 120c81.092 18.407 161.123 18.926 240 0l20-120c-58.317 0-221.607 0-280 0z" fill="#b7e8f9"></path>
						<path d="m376 325.999h-240l-80 160h400z" fill="#a9c9fb"></path>
						<path d="m196.35 325.999c2.45-17.064 17.11-30 34.65-30h5c16.57 0 30-13.43 30-30 31.62 0 55.392 29.139 48.99 60-4.599 22.742-24.754 40-48.99 40-12 8.333-23.667 8.333-35 0-19.33 0-35-15.67-35-35z" fill="#ea9b58"></path>
						<path d="m311 365.999c19.33 0 35 15.67 35 35 0 19.343-15.679 35-35 35h-110c-19.33 0-35-15.67-35-35 0-19.343 15.679-35 35-35h65z" fill="#d88a55"></path>
						<path d="m376 335.999h-61.01c-5.522 0-10-4.477-10-10 0-5.522 4.478-10 10-10h52.538l16.667-100h-256.39l16.667 100h51.878c5.523 0 10 4.478 10 10 0 5.523-4.477 10-10 10h-60.35c-4.889 0-9.061-3.534-9.864-8.356l-20-120c-1.012-6.071 3.666-11.644 9.864-11.644h280c6.167 0 10.882 5.542 9.864 11.644l-20 120c-.803 4.822-4.975 8.356-9.864 8.356z"></path>
						<path d="m456 495.999h-400c-7.418 0-12.268-7.825-8.944-14.472l80-160c1.694-3.389 5.156-5.528 8.944-5.528h60.35c5.523 0 10 4.478 10 10 0 5.523-4.477 10-10 10h-54.169l-70 140h367.639l-70-140h-54.83c-5.522 0-10-4.477-10-10 0-5.522 4.478-10 10-10h61.01c3.788 0 7.25 2.14 8.944 5.528l80 160c3.32 6.64-1.517 14.472-8.944 14.472z"></path>
						<path d="m446.222 488.095-60-280c-1.157-5.4 2.283-10.717 7.683-11.874 5.398-1.155 10.717 2.283 11.874 7.683l60 280c1.157 5.4-2.283 10.717-7.683 11.874-5.377 1.152-10.712-2.263-11.874-7.683z"></path>
						<path d="m53.905 495.777c-5.399-1.157-8.84-6.474-7.683-11.874l60-280c1.157-5.399 6.469-8.838 11.874-7.683 5.399 1.157 8.84 6.474 7.683 11.874l-60 280c-1.158 5.4-6.473 8.84-11.874 7.683z"></path>
						<path d="m311 445.999h-110c-24.814 0-45-20.186-45-45 0-24.813 20.186-45 45-45h110c24.814 0 45 20.187 45 45s-20.186 45-45 45zm-110-70c-13.785 0-25 11.215-25 25s11.215 25 25 25h110c13.785 0 25-11.215 25-25s-11.215-25-25-25z"></path>
						<path d="m266 375.999h-35c-24.814 0-45-20.186-45-45 0-24.813 20.186-45 45-45h5c11.028 0 20-8.972 20-20 0-5.522 4.478-10 10-10 33.084 0 60 26.916 60 60s-26.916 60-60 60zm-35-70c-13.785 0-25 11.215-25 25s11.215 25 25 25h35c22.056 0 40-17.944 40-40 0-19.145-13.519-35.19-31.511-39.094-4.759 16.773-20.212 29.094-38.489 29.094z"></path>
						<path d="m296 215.999h-80c-5.523 0-10-4.478-10-10v-140c0-27.57 22.43-50 50-50s50 22.43 50 50v140c0 5.522-4.477 10-10 10zm-70-20h60v-130c0-16.542-13.458-30-30-30s-30 13.458-30 30z"></path>
						<path d="m296 105.999h-80c-5.523 0-10-4.478-10-10s4.477-10 10-10h80c5.522 0 10 4.478 10 10s-4.477 10-10 10z"></path>
						<path d="m296 145.999h-80c-5.523 0-10-4.478-10-10 0-5.523 4.477-10 10-10h80c5.522 0 10 4.478 10 10s-4.477 10-10 10z"></path>
					</g>
				</svg>
			</button>
		</div>
	</div>
	
</template>

<style>

</style>