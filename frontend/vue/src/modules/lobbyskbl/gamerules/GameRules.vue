<script setup>
    import { ref, onMounted, onUnmounted, watch } from 'vue';
    import { getCookie }            from '@shared';

    let roomCode = ref('Default');
    let roomName = ref('Default');
    let username = ref('');
    let users    = ref([]);

    let inputRoomName = ref('');
    let inputRoomCode = ref('');
    let gameStarted   = ref(false);
    let seeRoomInfo   = ref(false);

    onMounted(() => {
        getUserRoomInfo();
    });

    onUnmounted(() => {
        
    });

    // watch(message, (newMessage) => {

    // });

    const getUserRoomInfo = async () => {
        users.value = [];
        try {
            const response = await fetch('/api/users/me');
            const dataUser = await response.json();
            if (dataUser.skribble) {
                username.value = dataUser.username;
                roomCode.value = dataUser.skribble.code;
                roomName.value = dataUser.skribble.name;
                gameStarted.value = dataUser.skribble.game_started;
                dataUser.skribble.players.forEach(element => {
                    users.value.push(element.username);
                });
                seeRoomInfo.value = true;
            } else {
                seeRoomInfo.value = false;
            }
        } catch (error) {
            console.error("Recuperation error :", error);
        }
    };

    const postCreateRoom = async () => {
		try {
			const response = await fetch('/api/skribble/rooms/', {
				method: 'POST',
				body: JSON.stringify({
                    name: inputRoomName.value
				}),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'Content-type' : 'application/json'
				}
			});
            if (response.ok) {
                inputRoomName.value = '';
                getUserRoomInfo();
                window.location.href = '/lobbyskbl'
            }
		} catch (error) {
			console.error("Creation error :", error);
		}
	};

    const postJoinRoom = async () => {
		try {
			const response = await fetch(`/api/skribble/rooms/${inputRoomCode.value}/join/`, {
				method: 'POST',
				body: JSON.stringify({
                    name: ''
				}),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'Content-type' : 'application/json'
				}
			});
            if (response.ok) {
                inputRoomCode.value = '';
                getUserRoomInfo();
                window.location.href = '/lobbyskbl'
            }
		} catch (error) {
			console.error("Join error :", error);
		}
	};

    const postLeaveRoom = async () => {
		try {
			const response = await fetch('/api/skribble/rooms/leave/', {
				method: 'POST',
				body: JSON.stringify({
                    name: ''
				}),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'Content-type' : 'application/json'
				}
			});
            if (response.ok) {
                getUserRoomInfo();
                window.location.href = '/lobbyskbl'
            }
		} catch (error) {
			console.error("Leave error :", error);
		}
	};

    const postStartGame = async () => {
		try {
			const response = await fetch(`/api/skribble/rooms/${roomCode.value}/start_game/`, {
				method: 'POST',
				body: JSON.stringify({
                    name: ''
				}),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'Content-type' : 'application/json'
				}
			});
            if (response.ok) {
                window.location.href = `/skribbl?room=${roomCode.value}`;
            }
		} catch (error) {
			console.error("Leave error :", error);
		}
	};
    
</script>

<template>
    <div class="flex justify-center h-full w-full">
        <div class="flex flex-col
            bg-navbar border-solid border-8 border-navbar
            gap-4 w-2xl h-9/10">
            <div class="flex justify-center
                gap-4 w-full">
                <h1 class="text-navbar-menu font-bold">GAME RULES</h1>
            </div>
            <div class="flex flex-col
                bg-white
                gap-4 w-full h-full">
                <div>
                    <div>Create Room:</div>
                    <div class="flex">
                        <input v-model="inputRoomName" placeholder="Write your room name"/>
                        <button
                            @click="postCreateRoom"
                            class="bg-navbar-menu rounded-sm">CREATE ROOM</button>
                    </div>
                </div>
                <div>
                    <div>Join Room:</div>
                    <div class="flex">
                        <input v-model="inputRoomCode" placeholder="Write your room code"/>
                        <button
                            @click="postJoinRoom"
                            class="bg-navbar-menu rounded-sm">JOIN ROOM</button>
                    </div>
                </div>
                <div class="flex flex-row">
                    <div>Leave Room:</div>
                    <div>
                        <button
                            @click="postLeaveRoom"
                            class="bg-red-600 rounded-sm">LEAVE ROOM</button>
                    </div>
                </div>
                <div class="flex flex-row">
                    <div>Game Start:</div>
                    <div>
                        <button
                            @click="postStartGame"
                            class="bg-green-600 rounded-sm">Start Game</button>
                    </div>
                </div>
                <div v-if="seeRoomInfo">
                    <div class="text-center">__________ROOM INFO__________</div>
                        <div>Room Code: {{ roomCode }}</div>
                        <div>Room Name: {{ roomName }}</div>
                        <div>Game Started: {{ gameStarted }}</div>
                        <div>Users in lobby:</div>
                    <div class="flex flex-row gap-4">
                        <div v-for="(user, index) in users">
                            <div>Avatar: </div>
                            <div class="bg-navbar-menu">Username{{ index + 1 }}: {{ user }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</template>