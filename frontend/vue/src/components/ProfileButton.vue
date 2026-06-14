<template>
  <button class="size-10 rounded-full overflow-hidden outline-0
    hover:outline-4 outline-navbar-profile-outline duration-150">
    <img 
      :src="profilePic" 
      alt="profile_pic"
      loading="eager"
    >
  </button>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { useUserStore }     from '@storage';
import defaultCat           from '@assets/default_cat.png'
import { storeToRefs }      from 'pinia';

const userStore         = useUserStore();
const { getProfilePic } = storeToRefs(userStore);
const profilePic        = ref(getProfilePic ?? defaultCat);
</script>
