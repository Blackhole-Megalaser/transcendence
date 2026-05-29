<template>
  <ul class="overflow-auto max-h-60">
    <li 
      class="w-full flex items-center flex-col rounded-xl overflow-hidden my-1 group"
      :key="friend.username"
      v-for="friend in FriendRequests"
      >
      <div 
        class="flex items-center flex:none gap-4 w-full z-10 px-4 py-2 hover:bg-button-2-active"
      >
        <div class="relative">
          <a :href="`users/${friend.username}`">
            <img
              alt="Profile Picture"
              class="size-10 z-11 rounded-full cursor-pointer"
              :src="friend.profilePicture"
            >
            <div
              class="size-3 rounded-full z-11 absolute right-0.5 top-0.5"
              :class="friend.isLogged ? 'bg-green-500' : 'bg-red-600'"
            ></div>
          </a>
        </div>
        <p class="text-text-main text-lg font-semibold truncate max-w-44 flex-1">{{ friend.username }}</p>
        <div class="hidden group-hover:flex flex-none gap-2 right-0">
          <component :is="check" class="size-4 cursor-pointer"/>
          <component :is="cross" class="size-4 fill-red-600 cursor-pointer"/>
        </div>
      </div>
    </li>
  </ul>
  <div 
    class="text-text-main font-semibold w-full py-2 flex-center"
    v-if="FriendRequests.length === 0"
  >
    <p>No incoming Friend Requests !</p>
  </div>
</template>

<script setup>
import { ref, computed }  from 'vue';
import default_cat        from '@assets/default_cat.png'
import cross              from '@assets/wrong_cross.svg'
import check              from '@assets/check-mark.svg'

const FriendRequests = ref([
  {
    profilePicture: default_cat,
    username:       'lab_cat_lsjglkjlwkgjwlgkjwwjvkvoweijvwe1',
    isLogged:       true
  },
  {
    profilePicture: default_cat,
    username:       'lab_cat_2',
    isLogged:       false
  }
])
</script>

<style scoped>
</style>
