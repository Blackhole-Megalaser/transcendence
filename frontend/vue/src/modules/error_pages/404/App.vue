<template>
  <BasePage>
    <div class="flex-center gap-10 lg:gap-4 xl:gap-10 flex-col w-full h-full font-bold italic">
      <h2 class="text-title text-3xl md:text-5xl text-center">Catsan Cat not found <br class="lg:hidden">:(<br>(404)</h2>
      <img src="@assets/catsan_cat.avif" alt="lost cat" class="h-1/2 xl:h-2/3">
    </div>
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
@import "@/style.css";

br {
  @apply mb-2
}
</style>
