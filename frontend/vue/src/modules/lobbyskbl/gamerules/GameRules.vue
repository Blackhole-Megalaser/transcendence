<template>
  <div class="flex justify-center h-full w-full">
    <div class="flex flex-col bg-navbar border-solid border-8 border-navbar gap-4 w-2xl h-9/10">
      <div class="flex justify-center gap-4 w-full">
        <h1 class="text-navbar-menu font-bold">GAME RULES</h1>
      </div>
      <div class="flex flex-col bg-white gap-4 w-full h-full">
        <div>
          <div>Create Room:</div>
          <div class="flex">
            <input v-model="inputRoomName" placeholder="Write your room name"/>
            <button
              @click="postCreateRoom"
              class="bg-navbar-menu rounded-sm"
            >CREATE ROOM</button>
          </div>
        </div>
        <div>
          <div>Join Room:</div>
          <div class="flex">
            <input v-model="inputRoomCode" placeholder="Write your room code"/>
            <button
                @click="postJoinRoom"
                class="bg-navbar-menu rounded-sm"
              >JOIN ROOM</button>
          </div>
        </div>
        <div class="flex flex-row">
          <div>Leave Room:</div>
          <div>
            <button
              @click="postLeaveRoom"
              class="bg-red-600 rounded-sm"
            >LEAVE ROOM</button>
          </div>
        </div>
        <div class="flex flex-row">
          <div>Game Start:</div>
          <div>
            <button
              @click="postStartGame"
              class="bg-green-600 rounded-sm"
            >Start Game</button>
          </div>
        </div>
        <div v-if="seeRoomInfo">
          <div class="text-center">__________ROOM INFO__________</div>
            <div>Room Code: {{ roomCode }}</div>
            <div>Room Name: {{ roomName }}</div>
            <div>Game Started: {{ gameStarted }}</div>
            <div>Host: {{ host }}</div>
            <div>isHost: {{ isHost }}</div>
            <!-- input + button => trigger postConfigure -->
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

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { storeToRefs }                        from 'pinia';							
import { useSkribbleStore, getCookie }        from '@shared';							

let roomCode = ref('Default');
let roomName = ref('Default');
let username = ref('');
let users    = ref([]);

let inputRoomName = ref('');
let inputRoomCode = ref('');
let gameStarted   = ref(false);
let seeRoomInfo   = ref(false);
let host          = ref('');
let isHost        = computed(() => {
  return username.value !== '' && username.value === host.value;
});
// let inputConfig   = ref('');

const skribbleStore = useSkribbleStore();
const {
  isConnected,
  isConnecting
} = storeToRefs(skribbleStore);

onMounted(() => {
  getUserRoomInfo();
});

onUnmounted(() => {
    
});

const handleLobbyMessage = async (e) => {
  if (!e.data) return;
  try {
    const message = JSON.parse(e.data);
    
    if (message.type === "update_players") {
      await getUserRoomInfo();
    }
      
    if (message.type === "game_started") {
      window.location.href = `/skribbl?room=${roomCode.value}`;
    }

  } catch (error) {
    console.error("Error lobby websocket:", error);
  }
};

const getUserRoomInfo = async () => {
  users.value = [];
  try {
    const response = await fetch('/api/users/me');
    const dataUser = await response.json();
    if (dataUser.skribble) {
      username.value = dataUser.username;
      host.value = dataUser.skribble.host;
      roomCode.value = dataUser.skribble.code;
      roomName.value = dataUser.skribble.name;
      gameStarted.value = dataUser.skribble.game_started;
      users.value = dataUser.skribble.players.map(element => element.username);
      seeRoomInfo.value = true;
      skribbleStore.connectWebSocket(roomCode.value, handleLobbyMessage);
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
        name: inputRoomName.value,
      }),
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type' : 'application/json'
      }
    });
    if (response.ok) {
        inputRoomName.value = '';
        await getUserRoomInfo();
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
        await getUserRoomInfo();
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
      seeRoomInfo.value = false;
      if (skribbleStore.socket) {
        skribbleStore.socket.close();
        skribbleStore.socket = null;
      }
      users.value = [];
    }
  } catch (error) {
    console.error("Leave error :", error);
  }
};

  const postStartGame = async () => {
  try {
    const response = await fetch(`/api/skribble/rooms/${roomCode.value}/start_game/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type' : 'application/json'
      }
    });
  } catch (error) {
    console.error("Leave error :", error);
  }
};

  const postConfigure = async () => {
  try {
    const response = await fetch(`/api/skribble/rooms/${roomCode.value}/configure/`, {
      method: 'POST',
      body: JSON.stringify({
        name: ''
      }),
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type' : 'application/json'
      }
    });
  } catch (error) {
    console.error("Leave error :", error);
  }
};
</script>
