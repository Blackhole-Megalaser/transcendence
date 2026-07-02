<template>
  <ul 
    class="overflow-auto max-h-60"
    v-if="friendList?.length > 0"
  >
    <li
      class="w-full flex items-center flex-col rounded-xl overflow-hidden my-1"
      v-for="friend in friendList"
      :key="friend.username"
    >
      <div
        class="flex items-center gap-4 w-full z-10 cursor-pointer px-4 py-2 hover:bg-button-2-active"
        @click="toggleOpen(friend.username)"
        :class="isOpen(friend.username) ? 'bg-button-2-active' : ''"
      >
        <div class="relative">
          <div class="relative z-11 size-10 rounded-full overflow-hidden cursor-pointer">
            <div 
              class="absolute inset-0 bg-cover bg-center"
              :style="{ backgroundImage: `url(${friend.profile_image})` }"
            />
          </div>
          <div
            class="size-3 rounded-full z-11 absolute right-0 bottom-0 border-2 border-navbar"
            :class="isLogged(friend.last_seen) ? 'bg-green-500' : 'bg-red-600'"
          ></div>
        </div>
        <p class="text-text-main text-lg font-semibold truncate max-w-52">{{ friend.username }}</p>
      </div>
      <div
        class="grid transition-all duration-300 ease-in-out w-full bg-button-sidebar-1-hover"
        :class="isOpen(friend.username) ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
      >
        <div
          class="font-semibold overflow-hidden flex items-center w-full transition-all duration-300 ease-in-out cursor-pointer"
          >
          <button
            class="px-4 cursor-pointer text-text-main w-full flex items-center justify-center text-center hover:bg-button-sidebar-2-active"
            :class="isOpen(friend.username) ? 'py-2' : 'py-0'"
            @click="deleteFriend(friend.username)"
          >Delete Friend</button>
        </div>
      </div>
    </li>
  </ul>
  <div
    class="text-text-main font-semibold w-full py-2 flex-center"
    v-else
    @click="console.log(friendList)"
  >
    <p>No Friends ! :c</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject } from 'vue';
import { storeToRefs }              from 'pinia';

import { getCookie }                from '@shared';
import { useUserStore }             from '@storage';
import default_cat                  from '@assets/default_cat.png';

const userStore         = useUserStore();
const { userInfos }     = storeToRefs(userStore);
const friends           = inject('FRIENDREQUESTS');
const friendList        = computed(() => [...friends.value.friends].sort((a, b) => a.username.localeCompare(b.username)));
const openFriends        = ref(new Set());
const isOpen            = (username) => openFriends.value.has(username);
const currentTimestamp  = ref(Date.now());
let   logStatusInterval = null;

const isLogged        = (lastActivityTimeISO) => {
  if (!lastActivityTimeISO) return (false);
  const lateTimestamp    = Date.parse(lastActivityTimeISO);
  return (currentTimestamp.value - lateTimestamp <= 4 * 60 * 1000);
}

const toggleOpen  = (username) => {
  const nextOpen  = new Set(openFriends.value);
  if (nextOpen.has(username)) {
    nextOpen.delete(username);
  } else {
    nextOpen.add(username);
  }
  openFriends.value = nextOpen;
}

const deleteFriend  = async (username) => {
  try {
    const response  = await fetch('/api/users/me/friends_request/', {
      method: 'POST',
      headers: { 
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type': 'application/json'
       },
      body: JSON.stringify({
        username: username,
        action: 'remove_friend'
      })
    })
    if (!response.ok) {
      const apiResponse = await response.json();
      throw ("Friend request error: " + apiResponse.detail);  
    }
    friends.value = {
      ...friends.value,
      friends: friends.value.friends.filter(w => w.username !== username)
    } 
    userStore.removeFriend(username);
  }
  catch (e) {
    console.error(e);
  }
}

onMounted(() => {
  logStatusInterval = setInterval(() => {
    currentTimestamp.value = Date.now();
  }, 10 * 1000)
})
onUnmounted(() => {
  clearInterval(logStatusInterval);
})
</script>
