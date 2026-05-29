<template>
  <ul>
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
            class="size-10 z-11 rounded-full"
            :src="friend.profilePicture"
          >
          <div 
            class="size-3 rounded-full z-11 absolute right-0.5 top-0.5"
            :class="friend.isLogged ? 'bg-green-500' : 'bg-red-600'"
          ></div>
        </div>
        <p class="text-text-main text-lg font-semibold">{{ friend.username }}</p>
      </div>
      <div 
        class="grid transition-all duration-300 ease-in-out w-full bg-button-sidebar-1-hover"
        :class="friend.isOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
      >
        <div 
          class="font-semibold overflow-hidden flex items-center w-full transition-all duration-300 ease-in-out cursor-pointer"
          >
          <button 
            class="px-4 text-text-main w-1/2 hover:bg-button-sidebar-2-active"
            :class="friend.isOpen ? 'py-2' : 'py-0'"
          >See Profile</button>
          <button 
            class="px-4 text-text-main w-1/2 hover:bg-button-sidebar-2-active"
            :class="friend.isOpen ? 'py-2' : 'py-0'"
          >Delete Friend</button>
        </div>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, computed }  from 'vue';
import default_cat        from '@assets/default_cat.png'

const friendList = ref([
  {
    profilePicture: default_cat,
    username:       'lab_cat_1',
    isLogged:       true,
    isOpen:         false
  },
  {
    profilePicture: default_cat,
    username:       'lab_cat_2',
    isLogged:       false,
    isOpen:         false
  }
])
</script>

<style scoped>
</style>
