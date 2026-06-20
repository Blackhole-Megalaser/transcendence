<script setup>
    import { ref, onMounted, onUnmounted, computed } from 'vue';
    import bucket from '@modules/skribbl/game/bucket.png'

    const width 		= ref(1000);
    const height 		= ref(500);
    const canvasRef 	= ref(null);
    const vueCanvas 	= ref(null);
    let resizeObserver 	= null;

    const isDrawing 	= ref(false);
    const isBucket 		= ref(false);
    const coord 		= ref({x: 0, y: 0});
    const penColor 		= ref('#000000');
    const penStroke 	= ref('4');
    let penSizeActive 	= ref('1');
    const paintColors 	= ref(['#3b82f6', '#ef4444', '#22c55e','#eab308', '#000000', '#ec4899', '#8b5cf6', '#854d0e', '#6b7280', '#ffffff']);
    const paletteRGB 	= [
		{ r: 59,  g: 130, b: 246, hex: '#3b82f6'}, // Blue
		{ r: 239, g: 68,  b: 68 , hex: '#ef4444'}, // Red
		{ r: 34,  g: 197, b: 94 , hex: '#22c55e'}, // Green
		{ r: 234, g: 179, b: 8  , hex: '#eab308'}, // Yellow
		{ r: 0,   g: 0,   b: 0  , hex: '#000000'}, // Black
		{ r: 236, g: 72,  b: 153, hex: '#ec4899'}, // Pink
		{ r: 139, g: 92,  b: 246, hex: '#8b5cf6'}, // Purple
		{ r: 133, g: 77,  b: 14 , hex: '#854d0e'}, // Brown
		{ r: 107, g: 114, b: 128, hex: '#6b7280'}, // Gray
		{ r: 255, g: 255, b: 255, hex: '#ffffff'}  // White

	];

	const history		= ref([]); 
    let currentPath 	= null;

	const roomName    	= "skribble_test";
	let Socket        	= null;
	const isDrawer		= ref(false);
    
    onMounted(() => {
        vueCanvas.value = canvasRef.value.getContext("2d");
        resizeObserver 	= new ResizeObserver(resizeCanvas);
        resizeObserver.observe(canvasRef.value.parentElement);
		penColor.value 	= '#ffffff';
		fill(1,1);
		penColor.value 	= '#000000';
    	connectWebSocket();
    	intervalId = setInterval(sendCanvas, 3000);
    });

    onUnmounted(() => {
        if (resizeObserver) {
            resizeObserver.disconnect();
        }
        if (this.Socket) {
            this.Socket.close();
        }
        clearInterval(intervalId);
    });

	const connectWebSocket = () => {
		const protocol	= window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		const host    	= window.location.host;
	
    	const wsUrl     = `${protocol}//${host}/ws/skribble/${roomName}/`;
    	Socket          = new WebSocket(wsUrl);

    	Socket.onopen = (e) => {
    		console.log('Socket connected to ' + roomName);
    	}	

    	Socket.onerror = (e) => {
    		console.log("Failed to reach server");
    	}

    	Socket.onmessage = async (e) => {
			if (!e.data || isDrawing.value) {
			  return;
			}

			// JSON string
			if (typeof e.data === 'string') {
				try {
					const message = JSON.parse(e.data);
					
					if (message.type === "canvas.update" && message.blob_data) {
						const blobData = hexStringToBlob(message.blob_data, "image/png");
						await receiveCanvasBlob(blobData);
					}
				else if (message.type === "chat.message") {
				    receiveCanvas(message);
				  }
				else {
				    console.log("Unknown message type:", message.type);
				  }
				} catch (err) {
				  console.error("Failed to parse JSON message:", err);
				}
				return;
			}
	  
			// Blob (direct binary)
			if (e.data instanceof Blob) {
			try {
				await receiveCanvasBlob(e.data);
			}
			catch (err) {
				console.error("Failed to process canvas blob:", err);
			}
			return;
			}
		};

      Socket.onclose = (e) => {
        console.log('Socket closed');
      };
    };

    const sendCanvas = () => {

        if (!Socket || Socket.readyState !== WebSocket.OPEN || !isDrawer.value) {
           return;
        }

        canvasRef.value.toBlob(function(blob) {
        	if (Socket.readyState === WebSocket.OPEN) {
        	    Socket.send(blob);
        	}
      }, 'image/png', 0.9);

    };

    // text here
    const receiveCanvas = (e) => {

    	if (!Socket || Socket.readyState !== WebSocket.OPEN) {
    		return;
    	}
		console.log("Welcome to the other side");
    };

    // canvas here
    async function receiveCanvasBlob(blob) {
      return new Promise((resolve) => {

        const canvas = canvasRef.value;
        if (!canvas) {
          console.error("Canvas ref is null!");
          resolve();
          return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error("Canvas context is null!");
          resolve();
          return;
        }

        const reader = new FileReader();

        reader.onload = (event) => {
          const img = new Image();
        
          img.onload = () => {
            ctx.drawImage(img, 0, 0);
            resolve();
          };

          img.onerror = (err) => {
            console.error("Image failed to load:", err);
            resolve();
          };

          img.src = event.target.result;
        };

        reader.onerror = (err) => {
          console.error("FileReader error:", err);
          resolve();
        };

        reader.readAsDataURL(blob);
      });
    }

    function hexStringToBlob(hexString, type) {
    	const bytes = new Uint8Array(hexString.length / 2);
    	for (let i = 0; i < hexString.length; i += 2) {
    		bytes[i / 2] = parseInt(hexString.substr(i, 2), 16);
    	}
    	return new Blob([bytes], { type });
    }

    const resizeCanvas = () => {
        const canvas = canvasRef.value;
        if (!canvas) return;

        const rect = canvas.parentElement.getBoundingClientRect();

        const exactWidth 	= Math.floor(rect.width);
        const exactHeight	= Math.floor(rect.height);

        canvas.width		= exactWidth;
        canvas.height 		= exactHeight;
        width.value 		= exactWidth;
        height.value 		= exactHeight;

        redrawLines();
    };

    const reposition = (event) => {
        const canvas = canvasRef.value;
        if (!canvas) return;

        const rect 		= canvas.getBoundingClientRect();

        const xMouseRel = event.clientX - rect.left;
        const yMouseRel = event.clientY - rect.top;

        coord.value.x 	= xMouseRel * (canvas.width / rect.width);
        coord.value.y 	= yMouseRel * (canvas.height / rect.height);
    };
    
    const start = (event) => {
        reposition(event);
        
        if (isBucket.value) {
            fill(Math.floor(coord.value.x), Math.floor(coord.value.y));
            return;
        }
        isDrawing.value = true;
    
        currentPath = {
            type: 'paint',
            color: penColor.value,
            stroke: penStroke.value,
            points: [{ 
                x: coord.value.x / width.value,
                y: coord.value.y / height.value 
            }]
        };
    };
    
    const draw = (event) => {
        if (!isDrawing.value) return;
    
        const ctx = vueCanvas.value;
    
        ctx.beginPath();
        ctx.lineWidth 	= parseInt(penStroke.value);
        ctx.lineCap 	= 'round';
        ctx.lineJoin 	= 'round';
        ctx.strokeStyle = penColor.value;
    
        ctx.moveTo(coord.value.x, coord.value.y);
        reposition(event);
        ctx.lineTo(coord.value.x, coord.value.y);
        ctx.stroke();
    
        if (currentPath) {
            currentPath.points.push({ 
                x: coord.value.x / width.value, 
                y: coord.value.y / height.value 
            });
        }
    };
        
    const stop = () => {
        isDrawing.value = false;
        if (currentPath) {
            history.value.push(currentPath);
            currentPath = null;
        }
    };
    
    const clear = () => {
        vueCanvas.value.clearRect(0, 0, width.value, height.value);
        history.value = [];
    };

    const cursorStyle = computed(() => ({
        cursor: isBucket.value ? `url(${bucket}) 16 16, auto` : 'default'
    }));

	const hexToRgb = (hex) => {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return [r, g, b, 255];
    };

    const redrawLines = () => {
        const ctx = vueCanvas.value;
        if (!ctx) return;

        const currentWidth = width.value;
        const currentHeight = height.value;
    
        // ctx.clearRect(0, 0, currentWidth, currentHeight);
    
        history.value.forEach(action => {
            if (!action.type || action.type === 'paint') {
				if (action.points.length < 2) return;
			
				const baseStroke = action.stroke ? parseInt(action.stroke) : 4; 
				ctx.lineWidth 	 = baseStroke + 1.5; 
				
				ctx.lineCap		= 'round';
				ctx.lineJoin 	= 'round';
				ctx.beginPath();
				ctx.strokeStyle = action.color;
				
				ctx.moveTo(action.points[0].x * currentWidth, action.points[0].y * currentHeight);
				for (let i = 1; i < action.points.length; i++) {
					ctx.lineTo(action.points[i].x * currentWidth, action.points[i].y * currentHeight);
				}
				ctx.stroke();
			}
				
            if (action.type === 'fill') {
                const realX = Math.floor(action.x * currentWidth);
                const realY = Math.floor(action.y * currentHeight);
                runFillSilentlyOnContext(ctx, currentWidth, currentHeight, realX, realY, action.color);
            }
        });
    };
        
    const runFillSilentlyOnContext = (ctx, currentWidth, currentHeight, startX, startY, targetColor) => {
		if (startX < 0 || startX >= currentWidth || startY < 0 || startY >= currentHeight) return;
	
		const imageData = ctx.getImageData(0, 0, currentWidth, currentHeight);
		const data = imageData.data;
	
		const startPos = (startY * currentWidth + startX) * 4;
		const startR = data[startPos];
		const startG = data[startPos + 1];
		const startB = data[startPos + 2];
		const startA = data[startPos + 3];
		const paletteBorder = paletteRGB.filter(c => c.r !== startR || c.g !== startG || c.b !== startB);
		const [fillR, fillG, fillB] = hexToRgb(targetColor);
	
		if (startA === 255 && startR === fillR && startG === fillG && startB === fillB) return;
	
		const visited = new Uint8Array(currentWidth * currentHeight);
	
		const pixelStack = [[startX, startY]]; 
	
		const match = (x, y) => {
			const pos = (y * currentWidth + x) * 4;
			const r = data[pos];
			const g = data[pos + 1];
			const b = data[pos + 2];
			const a = data[pos + 3];
	
			if (startA < 10) {
				return a < 230;
			} else {
				for (let i = 0; i < paletteBorder.length; i++) {
					const c = paletteBorder[i];
					if (c.r === r && c.g === g && c.b === b) {
						return false;
					}
				}
				return true;
			}
		};
	
		while (pixelStack.length > 0) {
			const [cx, cy] = pixelStack.pop();
			let x = cx; 
			let y = cy;
	
			while (x >= 0 && match(x, y) && !visited[y * currentWidth + x]) x--;
			x++;
	
			let reachUp = false; 
			let reachDown = false;
	
			while (x < currentWidth && match(x, y) && !visited[y * currentWidth + x]) {
				const pos = (y * currentWidth + x) * 4;
				
				data[pos]	  = fillR; 
				data[pos + 1] = fillG; 
				data[pos + 2] = fillB; 
				data[pos + 3] = 255;
	
				visited[y * currentWidth + x] = 1;
	
				if (y > 0) {
					if (match(x, y - 1) && !visited[(y - 1) * currentWidth + x]) { 
						if (!reachUp) { 
							pixelStack.push([x, y - 1]); 
							reachUp = true; 
						} 
					} else if (reachUp) {
						reachUp = false;
					}
				}
				if (y < currentHeight - 1) {
					if (match(x, y + 1) && !visited[(y + 1) * currentWidth + x]) { 
						if (!reachDown) { 
							pixelStack.push([x, y + 1]); 
							reachDown = true; 
						} 
					} else if (reachDown) {
						reachDown = false;
					}
				}
				x++;
			}
		}
		ctx.putImageData(imageData, 0, 0);
	};
		
    const fill = (startX, startY) => {
        const ctx 			= vueCanvas.value;
        const currentWidth 	= width.value;
        const currentHeight = height.value;
        
        if (currentWidth <= 0 || currentHeight <= 0) return;
        if (startX < 0 || startX >= currentWidth || startY < 0 || startY >= currentHeight) return;
    
        runFillSilentlyOnContext(ctx, currentWidth, currentHeight, startX, startY, penColor.value);
        
        history.value.push({
            type: 'fill',
            x: startX / currentWidth,
            y: startY / currentHeight,
            color: penColor.value
        });
        
        redrawLines();
    };
</script>

<template>
	<div class="w-full h-full">
		<div class="grid grid-cols-2 lg:grid-cols-4 grid-rows-[3fr_1fr_1fr] lg:grid-rows-[1fr_0.30fr]
			gap-2 w-full h-full max-w-full max-h-full p-4
			bg-bg-main">
			<!-- __________ SCORES __________ -->
			<div class="order-2 lg:order-1 row-start-2 lg:row-start-1 
				w-full h-full min-h-0
				border-5 border-solid border-button-1-normal bg-white rounded-lg overflow-hidden">
				<div class="bg-white ">
					<p>SCORES</p>
					<p>TOP CANVAS</p>
				</div>
			</div>
			<!-- __________ CANVAS __________ -->
			<canvas :style="cursorStyle" ref="canvasRef"
				class="order-1 lg:order-2 col-span-2 lg:col-span-2 row-start-1
                     border-5 border-solid border-button-1-normal bg-white overflow-hidden rounded-lg
                     w-full h-full min-h-0 block"
				@mousedown="start"
				@mousemove="draw"
				@mouseup="stop"
				@mouseleave="stop">
			</canvas>
			<!-- __________ CHAT __________ -->
			<div class="order-3 row-start-2 lg:row-start-1
				w-full h-full min-h-0
				border-5 border-solid border-button-1-normal bg-white overflow-hidden rounded-lg">
				<div class="bg-white">
					<p>CHAT</p>
					<p>Hello my name is Big Bob</p>
				</div>
			</div>
			<!-- __________ COLORS __________ -->
			<div :style="[cursorStyle, {backgroundColor: penColor}]" 
				class="order-5 row-start-3 lg:row-start-2  col-start-1 lg:col-start-2
					grid grid-flow-col grid-rows-1 justify-center
					h-full w-full max-w-full max-h-full min-h-0 
					bg-sidebar border-5 border-solid rounded-full overflow-hidden border-button-1-normal">
				<button :style="[cursorStyle, {backgroundColor: penColor}]"
					class="bg-sidebar w-full h-full overflow-hidden">
					<svg class="stroke-[0.5]  w-full h-full"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse class="stroke-[0.7] stroke-[#917F97] fill-pink-50" cx="16" cy="18" rx="13" ry="15"/>
						<ellipse class="hover:stroke-blue-500 hover:fill-blue-400 stroke-blue-600 fill-blue-500" @click="penColor = paintColors[0]" cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-red-500 hover:fill-red-400 stroke-red-600 fill-red-500" @click="penColor = paintColors[1]" cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-green-500 hover:fill-green-400 stroke-green-600 fill-green-500" @click="penColor = paintColors[2]" cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-yellow-500 hover:fill-yellow-400 stroke-yellow-600 fill-yellow-500" @click="penColor = paintColors[3]" cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path class="hover:stroke-gray-800 hover:fill-gray-900 stroke-gray-800 fill-black" @click="penColor = paintColors[4]" d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
						<rect class="stroke-[#917F97] fill-pink-50" x="5.5" y="27" width="21" height="32"></rect>
						<rect class="fill-pink-50" x="5.75" y="26.5" width="20.5" height="32"></rect>
					</svg>
				</button>
				<button :style="[cursorStyle, {backgroundColor: penColor}]"
					class="bg-sidebar w-full h-full overflow-hidden">
					<svg class="stroke-[0.5]  w-full h-full"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse class="stroke-[0.7] stroke-[#917F97] fill-pink-50" cx="16" cy="18" rx="13" ry="15"/>
						<ellipse class="hover:stroke-pink-500 hover:fill-pink-400 stroke-pink-600 fill-pink-500" @click="penColor = paintColors[5]" cx="12.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-violet-500 hover:fill-violet-400 stroke-violet-600 fill-violet-500" @click="penColor = paintColors[6]" cx="19.5" cy="9.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-yellow-800 hover:fill-yellow-700 stroke-yellow-900 fill-yellow-800" @click="penColor = paintColors[7]" cx="7.5" cy="16.5" rx="2.5" ry="3.5"/>
						<ellipse class="hover:stroke-gray-500 hover:fill-gray-400 stroke-gray-600 fill-gray-500" @click="penColor = paintColors[8]" cx="24.5" cy="16.5" rx="2.5" ry="3.5"/>
						<path class="hover:stroke-gray-200 hover:fill-gray-50 stroke-gray-200 fill-white" @click="penColor = paintColors[9]" d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
						<rect class="stroke-[#917F97] fill-pink-50" x="5.5" y="27" width="21" height="32"></rect>	
						<rect class="fill-pink-50" x="5.75" y="26.5" width="20.5" height="32"></rect>
					</svg>
				</button>
			</div>
			<!-- __________ TOOLS __________ -->
			<div :style="{cursorStyle}" 
				class="order-5 row-start-3 col-start-2 lg:row-start-2 lg:col-start-3 grid grid-cols-4 grid-rows-2 overflow-hidden rounded-full
				w-full h-full max-w-full max-h-full min-h-0
				bg-sidebar border-5 border-solid border-button-1-normal">
				<button :style="cursorStyle" 
					class="col-span-1 col-end-2
					w-full h-full
					bg-sidebar hover:bg-navbar-menu flex justify-center" 
					@click="clear">
					<svg 
						class=" h-full w-full" 
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
				<button :style="cursorStyle"
					:class="isBucket ? 'bg-sidebar' : 'bg-theme-button'"
					class="hover:bg-navbar-menu w-full h-full" 
					@click="isBucket = false">
					<svg 
						xmlns="http://www.w3.org/2000/svg"
						class=" h-full w-full"
						viewBox="0 0 640 640">
						<path fill="rgb(116, 192, 252)" d="M512.5 74.3L291.1 222C262 241.4 243.5 272.9 240.5 307.3C302.8 320.1 351.9 369.2 364.8 431.6C399.3 428.6 430.7 410.1 450.1 381L597.7 159.5C604.4 149.4 608 137.6 608 125.4C608 91.5 580.5 64 546.6 64C534.5 64 522.6 67.6 512.5 74.3zM320 464C320 402.1 269.9 352 208 352C146.1 352 96 402.1 96 464C96 467.9 96.2 471.8 96.6 475.6C98.4 493.1 86.4 512 68.8 512L64 512C46.3 512 32 526.3 32 544C32 561.7 46.3 576 64 576L208 576C269.9 576 320 525.9 320 464z"/>
					</svg>
				</button>
				<button :style="cursorStyle"
					:class="isBucket ? 'bg-theme-button' : 'bg-sidebar'"
					class="col-start-3 col-end-4 hover:bg-navbar-menu" 
					@click="isBucket = true">
					<svg 
						xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
						class=" h-full w-full"
						viewBox="0 0 60 60"
						version="1.1">
						<title>016 - Paint Bucket</title><desc>Created with Sketch.</desc><defs/>
						<g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
							<g id="016---Paint-Bucket" fill-rule="nonzero">
								<path d="M59,22 C59,29.73 54.52,36 49,36 L28,36 C33.52,36 35,29.73 35,22 C35,14.56 33.85,8.48 28.62,8.03 C28.42,8.01 28.21,8 28,8 L49,8 C54.52,8 59,14.27 59,22 Z" id="Shape" fill="#7FACFA"/>
								<path d="M56,22 C56,29.73 51.52,36 46,36 L28,36 C33.52,36 35,29.73 35,22 C35,14.56 33.85,8.48 28.62,8.03 C28.42,8.01 28.21,8 28,8 L46,8 C51.52,8 56,14.27 56,22 Z" id="Shape" fill="#A4C2F7"/>
								<path d="M38,22 C38,29.73 33.52,36 28,36 C27.5022031,36.002814 27.0056941,35.9491373 26.52,35.84 C31.32,34.81 35,29.01 35,22 C35,14.99 31.3,9.17 26.49,8.16 C26.986634,8.05578147 27.4925534,8.00217412 28,8 C28.21,8 28.42,8.01 28.62,8.03 C33.85,8.48 38,14.56 38,22 Z" id="Shape" fill="#CAD9FC"/>
								<path d="M35,22 C35,29.01 31.32,34.81 26.52,35.84 L26.51,35.84 C26.36,35.81 26.22,35.78 26.08,35.74 C26.28,35.25 26.48,34.81 26.7,34.39 C27.4035507,33.1544235 28.4581088,32.1555515 29.73,31.52 C30.3810994,31.1412724 30.9572826,30.6464327 31.43,30.06 L31.44,30.06 C32.5741586,28.6180933 33.3426811,26.9232267 33.68,25.12 C33.76,24.72 33.83,24.3 33.88,23.87 C33.9614035,23.2500154 34.0014919,22.6253041 34,22 C34,16.11 30.84,12 28,12 C27.4784856,12.008562 26.9656734,12.1350557 26.5,12.37 C24.15,13.49 22,17.14 22,22 C21.9345593,24.6425976 22.6701107,27.2431727 24.11,29.46 C23.0651734,30.3179878 22.1132916,31.2832764 21.27,32.34 C20.79729,31.7439113 20.3821026,31.1043887 20.03,30.43 C18.6631612,27.8324113 17.9654575,24.9350506 18,22 C18,15.01 21.66,9.21 26.45,8.17 C26.46,8.17 26.48,8.16 26.49,8.16 C31.3,9.17 35,14.98 35,22 Z" id="Shape" fill="#E8EDFC"/>
								<path d="M41,51.5 C41,55.64 32.05,59 21,59 C20.49,59 19.99,58.99 19.5,58.98 C9.15,58.69 1,55.45 1,51.5 C1,47.86 7.9,44.83 17.07,44.14 L21.48,44.12 L24.2,44.1 L24.26,44.1 C33.76,44.68 41,47.78 41,51.5 Z" id="Shape" fill="#CAD9FC"/>
								<path d="M38,51.5 C38,55.45 29.85,58.69 19.5,58.98 C9.15,58.69 1,55.45 1,51.5 C1,47.86 7.9,44.83 17.07,44.14 L21.48,44.12 C30.87,44.73 38,47.81 38,51.5 Z" id="Shape" fill="#E8EDFC"/>
								<path d="M34,22 C34.0014919,22.6253041 33.9614035,23.2500154 33.88,23.87 C33.83,24.3 33.76,24.72 33.68,25.12 C31,26.06 27.19,26.96 24.11,29.46 C23.8862145,29.1430476 23.682483,28.8124014 23.5,28.47 C22.4819233,26.4671754 21.9670804,24.2464868 22,22 C22,16.8 24.46,12.99 27,12.17 C27.3220988,12.0602267 27.6597209,12.0028309 28,12 C30.84,12 34,16.11 34,22 Z" id="Shape" fill="#7FACFA"/>
								<path d="M32,22 C32.0014919,22.6253041 31.9614035,23.2500154 31.88,23.87 C31.83,24.3 31.76,24.72 31.68,25.12 C29.39,25.92 26.28,26.7 23.5,28.47 C22.4819233,26.4671754 21.9670804,24.2464868 22,22 C22,16.8 24.46,12.99 27,12.17 C29.54,12.99 32,16.8 32,22 Z" id="Shape" fill="#CAD9FC"/>
								<path d="M33.68,25.12 C33.3426811,26.9232267 32.5741586,28.6180933 31.44,30.06 L31.43,30.06 C30.9572826,30.6464327 30.3810994,31.1412724 29.73,31.52 C28.4581088,32.1555515 27.4035507,33.1544235 26.7,34.39 C26.48,34.81 26.28,35.25 26.08,35.74 C25.4777165,37.2779013 25.0321269,38.8726431 24.75,40.5 C24.5036779,41.6895274 24.320091,42.8911873 24.2,44.1 C24.1001959,45.1190082 24.1780175,46.1476072 24.43,47.14 C24.6663982,48.0389002 25.1851987,48.8381334 25.91,49.42 C26.0725362,49.5323203 26.152518,49.7306808 26.113353,49.9243298 C26.074188,50.1179789 25.9234095,50.2696688 25.73,50.31 C23.588243,50.7649672 21.3974237,50.9464155 19.21,50.85 C18.72,50.82 18.23,50.78 17.73,50.71 C16.1434557,50.5162668 14.5750649,50.1952316 13.04,49.75 C12.8278277,49.6834645 12.6850891,49.4848061 12.6897206,49.2624942 C12.6943521,49.0401822 12.8452407,48.8476411 13.06,48.79 C14.3799575,48.3162009 15.4820368,47.3776559 16.16,46.15 C16.5341061,45.5143489 16.8391734,44.8405189 17.07,44.14 C17.78,42.08 17.99,39.85 18.54,37.74 C19.0583961,35.7673886 19.9888232,33.9269834 21.27,32.34 C22.1132916,31.2832764 23.0651734,30.3179878 24.11,29.46 C26.3094228,27.8166081 28.7948866,26.5959164 31.44,25.86 C32.24,25.6 33,25.36 33.68,25.12 Z" id="Shape" fill="#CAD9FC"/>
								<path d="M31.44,25.86 C31.0250037,27.0185895 30.4200723,28.1000311 29.65,29.06 L29.64,29.06 C29.1454994,29.6748284 28.5421278,30.1934568 27.86,30.59 C26.526841,31.2584661 25.4206301,32.3055399 24.68,33.6 C24.45,34.04 24.24,34.5 24.03,35.01 C23.398488,36.6218393 22.9327524,38.2937968 22.64,40 C22.42,41.22 22.16,42.5 22.06,43.77 C21.9585609,44.8392498 22.0397181,45.9179643 22.3,46.96 C22.5534514,47.9019141 23.0997554,48.7388798 23.86,49.35 C24.22,49.62 24.887,50.474 23.952,50.622 C22.3845399,50.8722722 20.7942407,50.9487353 19.21,50.85 C18.72,50.82 18.23,50.78 17.73,50.71 C16.1434557,50.5162668 14.5750649,50.1952316 13.04,49.75 C12.8278277,49.6834645 12.6850891,49.4848061 12.6897206,49.2624942 C12.6943521,49.0401822 12.8452407,48.8476411 13.06,48.79 C14.3799575,48.3162009 15.4820368,47.3776559 16.16,46.15 C16.5341061,45.5143489 16.8391734,44.8405189 17.07,44.14 C17.78,42.08 17.99,39.85 18.54,37.74 C19.0583961,35.7673886 19.9888232,33.9269834 21.27,32.34 C22.1132916,31.2832764 23.0651734,30.3179878 24.11,29.46 C26.3094228,27.8166081 28.7948866,26.5959164 31.44,25.86 Z" id="Shape" fill="#E8EDFC"/>
								<circle id="Oval" fill="#CAD9FC" cx="46" cy="22" r="2"/>
								<path d="M29.135,35.882 C28.985,35.852 28.845,35.822 28.705,35.782 C28.67,35.867 28.643,35.956 28.605,36.042 L30.621,36.042 C30.1232031,36.044814 29.6266941,35.9911373 29.141,35.882 L29.135,35.882 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M26.735,29.5 C26.5450392,29.2240618 26.3691481,28.9386977 26.208,28.645 C26.3689857,28.9387922 26.5448818,29.2241644 26.735,29.5 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M28.119,28.517 C28.019,28.583 27.919,28.646 27.813,28.717 C27.915,28.646 28.017,28.582 28.119,28.517 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M25.516,27.159 C25.670665,27.5624904 25.8482886,27.9568014 26.048,28.34 C25.8486996,27.9566021 25.6710866,27.5623147 25.516,27.159 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M19.125,59.022 C19.615,59.032 20.115,59.042 20.625,59.042 C21.088,59.042 21.541,59.027 21.996,59.016 C11.708,58.7 3.625,55.475 3.625,51.542 C3.625,47.902 10.525,44.872 19.695,44.182 C20.405,42.122 20.615,39.892 21.165,37.782 C21.6833961,35.8093886 22.6138232,33.9689834 23.895,32.382 C23.42229,31.7859113 23.0071026,31.1463887 22.655,30.472 C21.2881612,27.8744113 20.5904575,24.9770506 20.625,22.042 C20.625,15.052 24.285,9.252 29.075,8.212 C29.085,8.212 29.105,8.202 29.115,8.202 C29.611634,8.09778147 30.1175534,8.04417412 30.625,8.042 L27.625,8.042 C27.1175534,8.04417412 26.611634,8.09778147 26.115,8.202 C26.105,8.202 26.085,8.212 26.075,8.212 C21.285,9.252 17.625,15.052 17.625,22.042 C17.5904575,24.9770506 18.2881612,27.8744113 19.655,30.472 C20.0071026,31.1463887 20.42229,31.7859113 20.895,32.382 C19.6138232,33.9689834 18.6833961,35.8093886 18.165,37.782 C17.615,39.892 17.405,42.122 16.695,44.182 C7.525,44.872 0.625,47.902 0.625,51.542 C0.625,55.492 8.775,58.732 19.125,59.022 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M28,9 C27.0594301,9.02222951 26.1331206,9.23484185 25.277,9.625 C24.4015961,10.0418679 23.6059214,10.6087564 22.926,11.3 C21.5235576,12.7526559 20.4810236,14.5137302 19.882,16.442 C19.0536258,19.0074893 18.8063196,21.7251251 19.158,24.398 C19.4609744,27.053192 20.4615424,29.5808338 22.058,31.724 L20.484,32.96 C18.6666093,30.5345308 17.5248145,27.6705548 17.175,24.66 C16.7843874,21.6881067 17.0610964,18.6665136 17.985,15.815 C18.6818752,13.5885713 19.892052,11.5569952 21.518,9.884 C22.3621452,9.02763595 23.3497258,8.32570237 24.436,7.81 C25.5557194,7.29796756 26.768962,7.0222306 28,7 L28,9 Z" id="Shape" fill="#FFFFFF"/>
								<path d="M23.354,9.609 C23.6557905,10.0356942 24.22795,10.1711267 24.689,9.925 C25.6912738,9.32888779 26.8338915,9.00967265 28,9 L28,7 C26.4827095,7.00985713 24.9951632,7.42185673 23.689,8.194 C23.4454175,8.32676339 23.2697592,8.55681796 23.2058483,8.82676975 C23.1419375,9.09672154 23.1958006,9.3811151 23.354,9.609 Z" id="Shape" fill="#428DFF"/>
								<path d="M20.483,32.958 L22.057,31.722 C20.4605424,29.5788338 19.4599744,27.051192 19.157,24.396 C18.8053196,21.7231251 19.0526258,19.0054893 19.881,16.44 C19.989,16.14 20.074,15.84 20.198,15.555 C20.3859476,15.0525747 20.1543027,14.4902578 19.667,14.266 C19.4193158,14.1547822 19.136778,14.1503938 18.8857593,14.2538657 C18.6347405,14.3573376 18.4373652,14.5595501 18.34,14.813 C18.201,15.138 18.103,15.478 17.983,15.813 C17.0590964,18.6645136 16.7823874,21.6861067 17.173,24.658 C17.5231088,27.6686515 18.665252,30.5326359 20.483,32.958 Z" id="Shape" fill="#428DFF"/>
								<path d="M22.023,12.328 C22.169595,12.1257151 22.236524,11.8765112 22.211,11.628 L22.177,11.447 C22.1596647,11.3832857 22.134824,11.3218555 22.103,11.264 C22.0796941,11.205624 22.0483952,11.1507668 22.01,11.101 C21.9685854,11.0481873 21.9238269,10.9980845 21.876,10.951 C21.6750221,10.7708354 21.4104545,10.6783267 21.141,10.694 C21.0049615,10.7102621 20.8743667,10.7570984 20.759,10.831 C20.3856547,11.04221 20.1758361,11.4571143 20.227,11.883 C20.2527921,12.0146898 20.3048253,12.1398415 20.38,12.251 C20.4514116,12.3610564 20.5442577,12.4556029 20.653,12.529 C20.8735147,12.6686832 21.1365169,12.7253953 21.395,12.689 C21.6387848,12.6422042 21.859875,12.5151126 22.023,12.328 Z" id="Shape" fill="#428DFF"/>
								<path d="M28,37 C27.261545,36.9979185 26.5266896,36.897023 25.815,36.7 C25.5396085,36.6243927 25.3096822,36.4346495 25.1831905,36.1786089 C25.0566988,35.9225683 25.0457119,35.6246624 25.153,35.36 C25.359,34.851 25.58,34.37 25.811,33.928 C26.5994115,32.5122982 27.7956126,31.3666212 29.244,30.64 C29.78732,30.3234587 30.2671231,29.9087596 30.659,29.417 C30.6855176,29.3853357 30.7139014,29.3552822 30.744,29.327 C31.9622419,27.7033828 32.7042916,25.7725993 32.887,23.751 C32.9173738,23.3876298 33.143125,23.0695968 33.4761311,22.9210459 C33.8091372,22.772495 34.1966032,22.8169775 34.4872808,23.0371295 C34.7779585,23.2572816 34.9257635,23.6182003 34.873,23.979 C34.6463543,26.428078 33.7217725,28.7607035 32.209,30.7 C32.1808128,30.7355321 32.1500641,30.7689546 32.117,30.8 C31.5846068,31.442825 30.9410501,31.9847675 30.217,32.4 C29.1150386,32.9404423 28.1993331,33.7973059 27.587,34.861 C27.565,34.903 27.544,34.945 27.523,34.987 C27.682,35 27.842,35.006 28.002,35.006 C32.965,35.006 37.002,29.174 37.002,22.006 C37.002,14.838 32.963,9 28,9 C27.4477153,9 27,8.55228475 27,8 C27,7.44771525 27.4477153,7 28,7 C34.065,7 39,13.729 39,22 C39,30.271 34.065,37 28,37 Z" id="Shape" fill="#428DFF"/>
								<path d="M21.269,33.34 C20.885786,33.3397694 20.5364059,33.1205621 20.3694705,32.7756192 C20.2025352,32.4306763 20.2474072,32.0206704 20.485,31.72 C21.3719281,30.6079582 22.3734458,29.5923629 23.473,28.69 C23.7468248,28.450863 24.1288606,28.3791716 24.470754,28.5027652 C24.8126475,28.6263588 25.0605324,28.925765 25.1181495,29.2847173 C25.1757665,29.6436697 25.0340378,30.0056144 24.748,30.23 C23.7572607,31.0435695 22.854347,31.9585488 22.054,32.96 C21.8642631,33.2001097 21.5750274,33.3401218 21.269,33.34 Z" id="Shape" fill="#428DFF"/>
								<path d="M31.44,31.06 C31.0315258,31.0632513 30.6621386,30.8177339 30.5069836,30.43986 C30.3518286,30.0619861 30.4421018,29.6277321 30.735,29.343 C31.9582649,27.7172105 32.7035513,25.7823058 32.887,23.756 C32.9638666,23.1738497 33.0016179,22.5872009 33,22 C33,16.424 30.088,13 28,13 C25.912,13 23,16.424 23,22 C22.9344134,24.4374155 23.6071702,26.8377282 24.93,28.886 C25.2470114,29.3385974 25.1370973,29.9624885 24.6845,30.2795 C24.2319026,30.5965114 23.6080115,30.4865973 23.291,30.034 C21.7327728,27.6491558 20.9339913,24.8480162 21,22 C21,15.42 24.619,11 28,11 C31.381,11 35,15.42 35,22 C35.0018296,22.668803 34.9587326,23.3369737 34.871,24 C34.6420621,26.441806 33.7182753,28.7668892 32.209,30.7 C32.0188672,30.9282708 31.7370825,31.0601857 31.44,31.06 Z" id="Shape" fill="#428DFF"/>
								<path d="M49,9 L27.64,9 C27.0877153,9 26.64,8.55228475 26.64,8 C26.64,7.44771525 27.0877153,7 27.64,7 L49,7 C49.5522847,7 50,7.44771525 50,8 C50,8.55228475 49.5522847,9 49,9 Z" id="Shape" fill="#428DFF"/>
								<path d="M49,37 L28,37 C27.4477153,37 27,36.5522847 27,36 C27,35.4477153 27.4477153,35 28,35 L49,35 C49.5522847,35 50,35.4477153 50,36 C50,36.5522847 49.5522847,37 49,37 Z" id="Shape" fill="#428DFF"/>
								<path d="M49,37 C48.4477153,37 48,36.5522847 48,36 C48,35.4477153 48.4477153,35 49,35 C53.963,35 58,29.168 58,22 C58,14.832 53.963,9 49,9 C48.4477153,9 48,8.55228475 48,8 C48,7.44771525 48.4477153,7 49,7 C55.065,7 60,13.729 60,22 C60,30.271 55.065,37 49,37 Z" id="Shape" fill="#428DFF"/>
								<path d="M45.959,21 C45.42271,21.0004732 44.981524,20.577817 44.959,20.042 C44.8569718,16.0417337 44.0052345,12.0961309 42.448,8.41 C40.629,4.335 38.1,2 35.5,2 C32.9,2 30.371,4.335 28.553,8.408 C28.4072357,8.7341835 28.098527,8.95782513 27.7431616,8.99468124 C27.3877963,9.03153735 27.0397626,8.87600862 26.8301616,8.58668123 C26.6205606,8.29735383 26.5812356,7.91818349 26.727,7.592 C28.881,2.767 32.079,0 35.5,0 C38.921,0 42.119,2.767 44.273,7.592 C45.9353709,11.5092513 46.8465271,15.7040977 46.959,19.958 C46.9703724,20.2234447 46.8756434,20.4825033 46.6957208,20.6779979 C46.5157983,20.8734924 46.2654747,20.9893503 46,21 L45.959,21 Z" id="Shape" fill="#428DFF"/>
								<path d="M46,25 C44.7866133,25 43.6927044,24.2690735 43.2283614,23.1480503 C42.7640184,22.0270271 43.0206857,20.7366736 43.8786797,19.8786797 C44.7366736,19.0206857 46.0270271,18.7640184 47.1480503,19.2283614 C48.2690735,19.6927044 49,20.7866133 49,22 C49,23.6568542 47.6568542,25 46,25 Z M46,21 C45.4477153,21 45,21.4477153 45,22 C45,22.5522847 45.4477153,23 46,23 C46.5522847,23 47,22.5522847 47,22 C47,21.4477153 46.5522847,21 46,21 Z" id="Shape" fill="#428DFF"/>
								<path d="M21,60 C9.028,60 0,56.346 0,51.5 C0,46.61 8.536,43.779 17,43.143 C17.5447028,43.1110817 18.0144407,43.5216973 18.0556423,44.0657766 C18.0968439,44.6098559 17.6942977,45.0865271 17.151,45.137 C7.665,45.851 2,48.933 2,51.5 C2,54.574 9.8,58 21,58 C32.2,58 40,54.574 40,51.5 C40,48.885 33.959,45.694 24.2,45.1 C23.6477153,45.0665868 23.2270868,44.5917847 23.2605,44.0395 C23.2939132,43.4872153 23.7687153,43.0665868 24.321,43.1 C34.73,43.738 42,47.191 42,51.5 C42,56.346 32.972,60 21,60 Z" id="Shape" fill="#428DFF"/>
								<path d="M27,51 C26.8926115,51.0000777 26.7859116,50.9828571 26.684,50.949 C25.0856382,50.3797309 23.8769051,49.0501996 23.462,47.405 C23.0346929,45.2067147 23.1095566,42.9402949 23.681,40.775 L23.767,40.315 C24.0599438,38.6219434 24.5243337,36.9630732 25.153,35.364 C25.3606591,34.8520321 25.944032,34.605341 26.456,34.813 C26.9679679,35.0206591 27.214659,35.604032 27.007,36.116 C26.4296343,37.5901759 26.002797,39.1189502 25.733,40.679 L25.646,41.143 C25.1416007,43.0121757 25.0545436,44.9694236 25.391,46.876 C25.6366056,47.8731039 26.3561241,48.6860663 27.316,49.051 C27.781753,49.2057317 28.0663816,49.6755882 27.9878345,50.1600447 C27.9092874,50.6445013 27.4907827,51.0003557 27,51 Z" id="Shape" fill="#428DFF"/>
								<path d="M31.44,31.06 L31.43,31.06 C30.8786982,31.0572435 30.4336248,30.6088195 30.4350031,30.0575125 C30.4363814,29.5062055 30.8836913,29.0600125 31.435,29.0600125 C31.9863087,29.0600125 32.4336186,29.5062055 32.4349969,30.0575125 C32.4363752,30.6088195 31.9913018,31.0572435 31.44,31.06 Z" id="Shape" fill="#428DFF"/>
								<path d="M11.563,50.03 C11.3395062,50.030366 11.1161639,50.0183476 10.894,49.994 C10.345133,49.9352668 9.94766644,49.4429096 10.006,48.894 C10.0310794,48.629092 10.1619533,48.3854992 10.3690001,48.218356 C10.5760469,48.0512127 10.8417606,47.9746512 11.106,48.006 C12.8523044,48.1324143 14.5045147,47.2007316 15.3,45.641 C15.6385263,45.0661588 15.9144368,44.4566748 16.123,43.823 C16.5022221,42.6237725 16.7953012,41.3989893 17,40.158 C17.167,39.281 17.34,38.375 17.571,37.488 C18.1258049,35.3806644 19.1191168,33.4141453 20.486,31.717 C21.3725339,30.6061725 22.3733649,29.5915993 23.472,28.69 C25.9776725,26.8431185 28.8086395,25.4844579 31.817,24.685 C32.356,24.51 32.87,24.344 33.348,24.176 C33.8693568,23.9931938 34.4401937,24.2676432 34.623,24.789 C34.8058062,25.3103568 34.5313568,25.8811937 34.01,26.064 C33.518,26.236 32.988,26.408 32.433,26.587 C29.6653061,27.3186007 27.056776,28.555737 24.739,30.236 C23.7513923,31.0481419 22.8511885,31.9610813 22.053,32.96 C20.8599554,34.4396559 19.9924075,36.1543067 19.507,37.992 C19.292,38.815 19.133,39.649 18.965,40.533 C18.742383,41.8649475 18.4249085,43.1792921 18.015,44.466 C17.7615872,45.2303578 17.4280665,45.9657792 17.02,46.66 C15.9517193,48.6944763 13.8604717,49.9859377 11.563,50.03 Z" id="Shape" fill="#428DFF"/>
								<path d="M18.373,56.205 C11.49,56.205 7.673,53.968 7.485,53.857 C7.01877519,53.5700605 6.8699373,52.9615751 7.15107371,52.4918282 C7.43221011,52.0220813 8.03880323,51.8657099 8.512,52.141 C8.56,52.169 13.384,54.951 21.89,54.006 C22.438971,53.9452487 22.9332487,54.341029 22.994,54.89 C23.0547513,55.438971 22.658971,55.9332487 22.11,55.994 C20.8691906,56.1333487 19.6216091,56.2037902 18.373,56.205 Z" id="Shape" fill="#428DFF"/>
							</g>
						</g>
					</svg>
				</button>
				<button :style="cursorStyle"
					:class="penSizeActive === 1 ? 'bg-theme-button' : 'bg-sidebar'"
					class="flex justify-center col-start-1 hover:bg-navbar-menu"
					@click="penStroke = '4', penSizeActive = 1">
					<svg 
					xmlns="http://www.w3.org/2000/svg"
					class="h-full w-full"
					viewBox="0 0 100 100" 
					>
						<circle class="fill-button-sidebar-2-hover stroke-black stroke-2" cx="50" cy="50" r="25" />
						<circle class="fill-[#917F97]" cx="50" cy="50" r="22" />
						<circle class="fill-button-sidebar-2-hover" cx="50" cy="50" r="2" />
					</svg>			
				</button>
				<button :style="cursorStyle"
					:class="penSizeActive === 2 ? 'bg-theme-button' : 'bg-sidebar'"
					class="flex justify-center hover:bg-navbar-menu"
					@click="penStroke = '8', penSizeActive = 2">
					<svg 
					xmlns="http://www.w3.org/2000/svg"
					class="h-full w-full"
					viewBox="0 0 100 100" 
					>
						<circle class="fill-button-sidebar-2-hover stroke-black stroke-2" cx="50" cy="50" r="25" />
						<circle class="fill-[#917F97]" cx="50" cy="50" r="22" />
						<circle class="fill-button-sidebar-2-hover" cx="50" cy="50" r="4" />
					</svg>			
				</button>
				<button :style="cursorStyle"
					:class="penSizeActive === 3 ? 'bg-theme-button' : 'bg-sidebar'"
					class="flex justify-center 
					w-full h-full
					hover:bg-navbar-menu"
					@click="penStroke = '16', penSizeActive = 3">
					<svg 
					xmlns="http://www.w3.org/2000/svg"
					class="h-full w-full"
					viewBox="0 0 100 100" 
					>
						<circle class="fill-button-sidebar-2-hover stroke-black stroke-2" cx="50" cy="50" r="25" />
						<circle class="fill-[#917F97]" cx="50" cy="50" r="22" />
						<circle class="fill-button-sidebar-2-hover" cx="50" cy="50" r="8" />
					</svg>			
				</button>
				<button :style="cursorStyle"
					:class="penSizeActive === 4 ? 'bg-theme-button' : 'bg-sidebar'"
					class="flex justify-center hover:bg-navbar-menu"
					@click="penStroke = '32', penSizeActive = 4">
					<svg 
					xmlns="http://www.w3.org/2000/svg"
					class="h-full w-full"
					viewBox="0 0 100 100" 
					>
						<circle class="fill-button-sidebar-2-hover stroke-black stroke-2" cx="50" cy="50" r="25" />
						<circle class="fill-[#917F97]" cx="50" cy="50" r="22" />
						<circle class="fill-button-sidebar-2-hover" cx="50" cy="50" r="16" />
					</svg>			
				</button>
					<!-- <input type="range" min="4" max="20" step="2" 
					class="col-start-1 col-end-5 w-full h-25 bg-neutral-quaternary rounded-full appearance-none cursor-pointer"> -->
			</div>

		</div>
	</div>
		
	
</template>

<style>
	.bucket-cursor {
		cursor: 
			url("bucket.png"), auto;

	}
</style>
