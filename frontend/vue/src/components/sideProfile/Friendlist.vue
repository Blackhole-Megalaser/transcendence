<template>
  <ul class="overflow-auto max-h-60">
    <li
      class="w-full flex items-center flex-col rounded-xl overflow-hidden my-1"
      :key="friend.username"
      v-for="friend in friendList"
      >
      <div
        class="flex items-center gap-4 w-full z-10 cursor-pointer px-4 py-2 hover:bg-button-2-active"
        @click="friend.isOpen = !friend.isOpen"
        :class="friend.isOpen ? 'bg-button-2-active' : ''"
      >
        <div class="relative">
          <img
            alt="Profile Picture"
            class="size-10 min-w-10 z-11 rounded-full"
            :src="friend.profilePicture ?? default_cat"
          >
          <div
            class="size-3 rounded-full z-11 absolute right-0.5 top-0.5"
            :class="friend.isLogged ? 'bg-green-500' : 'bg-red-600'"
          ></div>
        </div>
        <p class="text-text-main text-lg font-semibold truncate max-w-52">{{ friend.username }}</p>
      </div>
      <div
        class="grid transition-all duration-300 ease-in-out w-full bg-button-sidebar-1-hover"
        :class="friend.isOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
      >
        <div
          class="font-semibold overflow-hidden flex items-center w-full transition-all duration-300 ease-in-out cursor-pointer"
          >
          <button
            class="px-4 cursor-pointer text-text-main w-full flex items-center justify-center text-center hover:bg-button-sidebar-2-active"
            :class="friend.isOpen ? 'py-2' : 'py-0'"
            @click="deleteFriend(friend.username)"
          >Delete Friend</button>
        </div>
      </div>
    </li>
  </ul>
  <div
    class="text-text-main font-semibold w-full py-2 flex-center"
    v-if="friendList.length === 0"
    @click="console.log(userInfos)"
  >
    <p>No Friends ! :c</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore }             from '@storage'
import { storeToRefs }              from 'pinia';
<<<<<<< HEAD
import { getCookie }                from '@shared';
import { useUserStore }             from '@storage';
import default_cat                  from '@assets/default_cat.png';
=======
import default_cat      from '@assets/default_cat.png'
>>>>>>> 76054ad (Update: now successfully see friends)

const userStore     = useUserStore();
const { userInfos } = storeToRefs(userStore);
const friendList    = computed(() => userInfos.value?.friendlist ?? []);

<<<<<<< HEAD
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
    userStore.removeFriend(username);
  }
  catch (e) {
    console.error(e);

  }
}

=======
>>>>>>> 76054ad (Update: now successfully see friends)
const logInfos  = () => {console.log(userInfos.value)}
</script>

<style scoped>
</style>
