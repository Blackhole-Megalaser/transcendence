<template>
  <div class="w-full relative">
    <div class="w-full h-auto bg-button-1-normal flex justify-center items-stretch rounded-t-2xl overflow-hidden font-semibold text-text-button-1">
      <button
        class="w-1/2 px-4 py-2 cursor-pointer"
        @click="bar = 0"
        :class="bar === 0 ? 'bg-button-1-active' : 'hover:bg-button-1-hover'"
      >Friendlist</button>
      <button
        class="w-1/2 relative px-4 py-2 cursor-pointer"
        @click="bar = 1"
        :class="bar === 1 ? 'bg-button-1-active' : 'hover:bg-button-1-hover'"
      >Friend requests
        <div
          class="size-3 absolute bg-red-600 top-1/2 right-2 -translate-y-1.5 rounded-full"
          v-if="friendRequests.length > 0"
        />
      </button>
    </div>
    <div class="w-full bg-navbar rounded-b-2xl px-4 py-2 shadow">
      <Friendlist v-if="selectWindow === 0"/>
      <FriendRequests v-else/>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject }  from 'vue';
import Friendlist                 from './Friendlist.vue';
import FriendRequests             from './FriendRequests.vue';

const bar             = ref(0);
const selectWindow    = computed(() => bar.value === 0 ? 0 : 1);
const friendData      = inject('FRIENDREQUESTS', ref({ friends: [], pending_friend_requests: [] }));
const friendRequests  = computed(() => friendData.value.pending_friend_requests);

</script>

<style scoped>
</style>
