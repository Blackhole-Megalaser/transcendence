<template>
  <div class="flex-center h-full w-full">
    <div class="flex flex-col bg-navbar lg:rounded-4xl p-4 md:p-8 gap-4 w-full h-full lg:w-2xl lg:h-9/10">
      <div class="flex justify-center gap-4 w-full">
        <h1 class="text-title font-bold text-4xl">~Game Rules~</h1>
      </div>

      <div class="h-px bg-navbar-border my-4 xl:my-0"></div>

      <div class="flex flex-col gap-4 w-full flex-1">

        <!-- First part: create or join -->
        <div 
          v-if="openFirst"
          class="rounded-2xl md:p-5 flex flex-col gap-5"
        >
          <div>
            <p class="text-title font-bold text-xl mb-2">Create a room</p>
            <div class="flex gap-2">
              <input
                v-model="inputRoomName"
                placeholder="Room name, ex: Room-1"
                class="informations flex-1"
                :disabled="seeRoomInfo"
              />
              <input
                type="submit"
                @click="postCreateRoom"
                class="input"
                :class="seeRoomInfo || inputRoomName === '' ? '' : 'cursor-pointer'"
                value="CREATE"
                :disabled="seeRoomInfo || inputRoomName === ''"
              >
            </div>
          </div>

          <div class="h-px bg-sidebar-border my-8 xl:my-0"></div>

          <div>
            <p class="text-title font-bold text-xl mb-2">Join a room</p>
            <div class="flex gap-2">
              <input
                v-model="inputRoomCode"
                placeholder="Room code, ex: IJJJK"
                class="informations flex-1"
                :disabled="seeRoomInfo"
              />
              <input
                type="submit"
                @click="postJoinRoom"
                class="input"
                :class="seeRoomInfo || inputRoomCode === '' ? '' : 'cursor-pointer'"
                value="JOIN"
                :disabled="seeRoomInfo || inputRoomCode === ''"
              >
            </div>
          </div>
        </div>

        <!-- Second Part: room log or empty box -->
        <div 
          v-if="openSecond"
          class="bg-lobby-room-bg rounded-2xl p-5 pb-2 md:pb-5 flex flex-col h-full text-text-main/70"
        >
          <template v-if="seeRoomInfo">
            <div class="flex items-center justify-between mb-4">
              <div>
                <p class="text-xs text-text-muted uppercase tracking-wide">Room code</p>
                <p class="text-xl font-mono font-medium">{{ roomCode }}</p>
              </div>
              <div 
                v-if="!gameStarted && isHost(username)"
                class="flex items-center gap-1"
              >
                <p class="w-18">Rounds : </p>
                <input 
                  type="text" 
                  class="informations w-20"
                  placeholder="Def: 3"
                  v-model="rounds"
                >
              </div>
              <div
                v-else-if="gameStarted" 
                class="flex items-center gap-1.5 bg-green-100 text-red-500 text-xs font-medium px-2.5 py-1 rounded-full"
              >
                Game Started
              </div>
            </div>

            <div class="flex-1 flex flex-col gap-1.5 overflow-y-auto max-h-56">
              <div
                v-for="(user, index) in users"
                :key="user"
                class="flex items-center gap-2.5 px-2.5 py-2 rounded-full bg-navbar"
              >
                <div class="size-7 rounded-full bg-title/15 flex-center text-xs font-medium">
                  {{ user.slice(0, 2).toUpperCase() }}
                </div>
                <span class="text-sm flex-1">{{ user }}</span>
                <p v-if="isHost(user)" class="pr-1" title="Host">👑</p>
              </div>
            </div>

            <div class="flex gap-2 mt-4 pt-4 border-t border-navbar-border">
              <button @click="postLeaveRoom" class="flex-1 btn-base btn-primary">
                Leave room
              </button>
              <button
                v-if="!gameStarted"
                @click="postStartGame" 
                class="flex-1 btn-base btn-secondary border border-text-main disabled:border-none"
                :disabled="!isHost(username)"
              >
                Start game
              </button>
              <a
                v-else
                :href="`/skribbl?room=${roomCode}`" 
                class="flex-1 btn-base btn-secondary border border-text-main"
              >
                Join room
            </a>
            </div>
          </template>

          <template v-else>
            <div class="flex-1 flex flex-col items-center justify-center text-center gap-2.5">
              <p class="text-sm font-medium">No room joined</p>
              <p class="text-xs text-text-muted max-w-56">Create a room or join one with a code to see who's here.</p>
            </div>
          </template>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { useBreakpoints }                               from '@vueuse/core'
import { storeToRefs }                        from 'pinia';							
import { useSkribbleStore, getCookie }        from '@shared';							

const breakpoints   = useBreakpoints({ xl: 1280 });
const isSmallScreen = breakpoints.smaller("xl");
const roomCode  = ref('Default');
const roomName  = ref('Default');
const username  = ref('');
const users     = ref([]);
const rounds    = ref(3);

const inputRoomName = ref('');
const inputRoomCode = ref('');
const gameStarted   = ref(false);
const seeRoomInfo   = ref(false);
const host          = ref('');
const openFirst     = computed(() => !isSmallScreen.value || !seeRoomInfo.value);
const openSecond    = computed(() => !isSmallScreen.value || seeRoomInfo.value);
const isHost        = (u) => u !== '' && u === host.value;
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
    console.log("Error lobby websocket:", error);
  }
};

const getUserRoomInfo = async () => {
  users.value = [];
  try {
    const response = await fetch('/api/users/me');
    if (!response.ok) throw new Error("Couldn't get User Room Infos");
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
    console.log("Recuperation error :", error);
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
    else 
      throw new Error("Couldn't create room");
  } catch (error) {
    console.log("Creation error :", error);
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
    else
      throw new Error("Couldn't join room");
  } catch (error) {
    console.log("Join error :", error);
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
    else  
      throw new Error("Couldn't leave room");
  } catch (error) {
    console.log("Leave error :", error);
  }
};

const postConfigure = async () => {
  const response = await fetch(`/api/skribble/rooms/${roomCode.value}/configure/`, {
    method: 'POST',
    body: JSON.stringify({
      // max_rounds: rounds.value 
      name: ''
    }),
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-type' : 'application/json'
    }
  });
  if (!response.ok) throw new Error("Couldn't configure game");
};

const postStartGame = async () => {
  try {
    await postConfigure();
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
    if (!status.ok) throw new Error("Couldn't start game");
  } catch (error) {
    console.log("Leave error :", error);
  }
};
</script>


<style scoped>
@import '@/style.css';

.input {
  @apply shadow-button-1-normal bg-button-1-normal text-text-button-1 hover:bg-button-1-hover disabled:bg-button-1-disable px-4 py-1 rounded-full mt-1;
}
.input:active:not(:disabled) {
  @apply duration-100 px-3.5 py-0.5;
}
.informations {
  @apply my-1 py-1 pl-3 h-10 text-text-main border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active focus:outline-none focus:ring-2 focus:ring-title
}
.btn-base {
  @apply px-4 py-2 md:px-6 rounded-full font-bold transition-all duration-300 shadow-xs;
}
.btn-primary {
  @apply shadow-button-1-normal;
  background-color: var(--color-button-1-normal);
  color: var(--color-text-button-1);
}
.btn-primary:hover:not(:disabled) {
  background-color: var(--color-button-1-hover);
}
.btn-primary:active:not(:disabled) {
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-1-active);
}
.btn-primary:disabled {
  background-color: var(--color-button-1-disable);
}
.btn-secondary {
  @apply shadow-button-2-normal;
  background-color: var(--color-button-2-variant);
  color: var(--color-text-button-2);
}
.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-button-2-hover);
}
.btn-secondary:active:not(:disabled) {
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-2-active);
}
.btn-secondary:disabled {
  background-color: var(--color-button-2-disable);
}
</style>
