<template>
  <button class="size-10 rounded-full overflow-hidden outline-0
    hover:outline-4 outline-navbar-profile-outline duration-150">
    <img :src="profilePicture !== '' ? profilePicture : defaultCat" alt="profile_pic">
  </button>
</template>

<script setup>
import { ref, watch } from 'vue';

import defaultCat from '@assets/default_cat.png'

defineProps({
  profilePicture: {
    type: String,
    default: ''
  }
})
</script>
