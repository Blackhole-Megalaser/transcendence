<template>
  <div class="w-full relative">
    <div class="w-full h-auto bg-button-1-normal flex justify-center items-stretch rounded-t-2xl overflow-hidden font-semibold text-text-button-1">
      <button 
        class="w-1/2 px-4 py-2" 
        @click="bar = 0"
        :class="bar === 0 ? 'bg-button-1-active' : 'hover:bg-button-1-hover'"
      >Friendlist</button>
      <button 
        class="w-1/2 px-4 py-2"
        @click="bar = 1"
        :class="bar === 1 ? 'bg-button-1-active' : 'hover:bg-button-1-hover'"
      >Friend requests</button>
    </div>
    <div class="w-full bg-navbar rounded-b-2xl px-4 py-2 shadow">
      <Friendlist v-if="selectWindow === 0"/>
      <FriendRequests v-else/>
    </div>
  </div>
</template>

<script setup>
import { ref, computed }  from 'vue';
import Friendlist         from './Friendlist.vue';
import FriendRequests     from './FriendRequests.vue';

const bar           = ref(0);
const selectWindow  = computed(() => bar.value === 0 ? 0 : 1)

</script>

<style scoped>
</style>
