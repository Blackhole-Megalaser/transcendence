<template>
  <BasePage>
    <TPlace class="z-40"/>
  </BasePage>
</template>

<script setup>
import { 
  onMounted,
  onUnmounted, 
  provide, 
  ref 
} from 'vue';
import { fetchFriends }  from '@shared';

const friendRequests  = ref([]);
let timer             = null;

provide('FRIENDREQUESTS', friendRequests);

const refreshFriendRequest = async () => {
  friendRequests.value = await fetchFriends(); 
}

onMounted(async () => {
  await refreshFriendRequest();
  timer = setInterval( refreshFriendRequest, 5000);
})

onUnmounted(() => {
  clearInterval(timer);
})
</script>

<style scoped>
</style>
