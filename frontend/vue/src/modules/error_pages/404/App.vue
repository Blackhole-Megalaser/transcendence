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

const friendInfos = ref({ status: '', friends: [], pending_friend_requests: []});
let   timer       = null;

provide('FRIENDREQUESTS', friendInfos);

const refreshFriendRequest = async () => {
  const result = await fetchFriends();
  if (result.status === 'ok') {
    friendInfos.value = result;
  } else {
    friendInfos.value = {
      ...friendInfos.value,
      status: 'error'
    }
  }
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
