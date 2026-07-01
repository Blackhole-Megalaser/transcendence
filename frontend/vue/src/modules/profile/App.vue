<template>
  <BasePage
    navBarVariant="home"
  >
    <Profile />
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
