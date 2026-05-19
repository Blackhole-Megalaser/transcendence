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
	<div class="flex justify-center bg-white">
		<div class="bg-white w-1/4 mr-10 ">
			<div class="grid grid-cols-1 justify-center bg-white border-4 border-solid border-red-500">
				<button @click="penColor = 'black'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-black hover:text-gray-800 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'gray'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-gray-500 hover:text-gray-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'blue'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-blue-500 hover:text-blue-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'red'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-red-500 hover:text-red-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'green'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-green-500 hover:text-green-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'yellow'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-yellow-500 hover:text-yellow-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'purple'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-purple-500 hover:text-purple-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'brown'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-yellow-900 hover:text-yellow-700 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
				<button @click="penColor = 'pink'" class="bg-pink-pastel-50">
					<svg class="w-12 h-12 text-pink-500 hover:text-pink-400 stroke-current fill-current"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
					</svg>
				</button>
			</div>
		</div>
		<canvas ref="canvasRef" :width="width" :height="height"
			class="border-4 border-solid border-red-500 bg-white"
			@mousedown="start"
			@mousemove="draw"
			@mouseup="stop"
			@mouseleave="stop">
		</canvas>
		<div class="bg-white w-1/4 h-full mr-10"></div>
	</div>
	<div class="flex flex-grid justify-center">
		<button class="text-white bg-gray-500" @click="clear">Clear</button>
	</div>
	
	
</template>

<style>

</style>