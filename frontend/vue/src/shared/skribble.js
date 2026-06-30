import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSkribbleStore = defineStore('skribble', () => {
	let socket = ref(null);
	const isConnected = ref(false);
	const isConnecting = ref(false);
	const connectionAttempt = ref(0);

	const history = ref([]);
	const tmpHistory = ref([]);
	const isDrawer = ref(false);

	const currentCode = ref(null);

	const connectWebSocket = (code, onMessageCallback = null) => {
		if (socket.value?.readyState === WebSocket.OPEN && currentCode.value === code) {
			isConnecting.value = false;
			isConnected.value = true;
			connectionAttempt.value = -1;
			return;
		}

		if (socket.value?.readyState === WebSocket.CONNECTING && currentCode.value === code) {
            return;
        }
		
		if (socket.value) {
			socket.value.close();
			socket.value = null;
		}
		currentCode.value = code;
		isConnecting.value = true;
		isConnected.value = false;
		connectionAttempt.value++;

		const protocol 	 = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		const host 		 = window.location.host;
		const wsUrl 	 = `${protocol}//${host}/ws/skribble/${code}/`;
	
		socket.value 		 = new WebSocket(wsUrl);
		isConnecting.value 	 = true;
	
		socket.value.onopen = () => {
			isConnecting.value = false;
			isConnected.value  = true;
		};

		if (onMessageCallback) {
            socket.value.onmessage = onMessageCallback;
        }
	
		socket.value.onerror = () => {
			isConnecting.value = false;
			isConnected.value  = false;
		};
	
		socket.value.onclose = () => {
			isConnecting.value = false;
			isConnected.value  = false;
		};
	};

	const sendAction = (payload) => {
		if (socket.value?.readyState === WebSocket.OPEN) {
			socket.value.send(JSON.stringify(payload));
		}
	};
	
	return {
		socket,
		isConnected,
		isConnecting,
		history,
		tmpHistory,
		isDrawer,
		currentCode,
		connectWebSocket,
		sendAction
	};
});