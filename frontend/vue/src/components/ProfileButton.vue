<template>
  <button class="group relative size-10 rounded-full overflow-hidden outline-0 hover:outline-4 outline-navbar-profile-outline duration-150">
    <div 
      class="absolute inset-0 bg-cover bg-center"
      :style="{ backgroundImage: `url(${profilePic})` }"
    />
  </button>
</template>

<script setup>
import { computed, onMounted, watchEffect } from 'vue';
import { useUserStore }     from '@storage';
import defaultCat           from '@assets/default_cat.png'
import { storeToRefs }      from 'pinia';

const userStore         = useUserStore();
const { getProfilePic } = storeToRefs(userStore);
const profilePic        = computed(() => getProfilePic.value ?? defaultCat);
</script>
