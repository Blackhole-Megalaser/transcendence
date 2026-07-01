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
        <div class="group relative size-10 rounded-full overflow-hidden">
          <div 
            class="absolute inset-0 bg-cover bg-center"
            :style="{ backgroundImage: `url(${friend.profile_image ?? default_cat})` }"
          />
        </div>
        <p class="text-text-main text-lg font-semibold truncate max-w-44 flex-1">{{ friend.username }}</p>
        <div
          class="flex md:hidden md:group-hover:flex flex-none gap-2 right-0"
        >
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
import { ref, computed, inject }  from 'vue';
import default_cat        from '@assets/default_cat.png'
import cross              from '@assets/wrong_cross.svg'
import check              from '@assets/check-mark.svg'

const FriendRequests = inject('FRIENDREQUESTS');
</script>

<style scoped>
</style>
