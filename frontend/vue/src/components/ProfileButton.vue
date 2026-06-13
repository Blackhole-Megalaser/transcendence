<template>
  <button class="size-10 rounded-full overflow-hidden outline-0
    hover:outline-4 outline-navbar-profile-outline duration-150">
    <img 
      :src="profilePic" 
      alt="profile_pic"
    >
  </button>
</template>

<script setup>
import { inject, onBeforeMount, ref } from 'vue';

import defaultCat from '@assets/default_cat.png'

const userInfos   = inject('userInfos', ref(null));
const profilePic  = ref(defaultCat);
const isLoaded    = ref(false);

onBeforeMount(() => {
  if (userInfos.value?.profile_image) {
    const userPicture = userInfos.value.profile_image;
    const imgLoader   = new Image();
    imgLoader.src     = userPicture;
    imgLoader.onload  = () => profilePic.value = userPicture;
  }
})
</script>
