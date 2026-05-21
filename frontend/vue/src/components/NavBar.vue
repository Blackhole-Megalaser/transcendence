<template>
  <nav class="flex justify-center relative">
    <div 
      class="flex items-center w-full h-20 bg-navbar border-b 
        border-navbar-border px-3 sm:px-6 shadow-md"
    >
      <div class="flex flex-none justify-start w-1/5">
        <button v-if="mobileProfile" class="flex-center" type="button" @click="$emit('changeStatus')">
          <component :is="currentPaw" class="fill-navbar-menu size-12" />
        </button>
      </div>
      <div class="h-20 flex flex-1 justify-center items-center sm:items-start">
        <a href="/" class="cursor-pointer" aria-label="back to home">
          <img 
            :src="themeIndex === 0 ? ft_cat : ft_mean" alt="LOGO"
            :class="`s-${variant}`"
          >
        </a>
      </div>
      <div class="flex flex-none justify-end w-1/5 items-center">
        <div v-if="mobileProfile" class="flex gap-5 lg:gap-10 ">
          <div class="hidden lg:flex">
            <ThemeButton />
          </div>
          <div class="hidden sm:max-lg:flex">
            <ThemeToggle />
          </div>
          <div class="flex items-center justify-end">
            <ProfileButton v-if="isLogged" 
              class="flex" @click="$emit('showProfile')"
            />
            <a v-else href="/" class="h-10 w-28 flex-center">
              <ButtonLogIn>
                Log in
              </ButtonLogIn>
            </a>
          </div>
        </div>
        <div v-else>
          <button @click="$emit('showProfile')" class="size-10 flex-center">
            <component :is=cross alt="close window" class="size-8" />
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useThemeStore } from '../storage/theme.js';
import { computed, ref } from 'vue';

import ButtonLogIn from './ButtonLogIn.vue';
import ProfileButton from './ProfileButton.vue';
import ThemeButton from './ThemeButton.vue';
import ThemeToggle from './ThemeToggle.vue';

import cross from '../assets/cross-svgrepo-com.svg'
import cute_paw from '../assets/cute_paw.svg?component';
import mean_paw from '../assets/mean_paw.svg?component';
import ft_cat from '../assets/ft_cat.png';
import ft_mean from '../assets/ft_cat-dark.png'

const theme = useThemeStore();
const themeIndex = computed (() => theme.getThemeIndex());
const currentPaw = computed (() => themeIndex.value === 0 ? cute_paw : mean_paw);
const emit = defineEmits(['changeStatus', 'showProfile']);
const isLogged = ref(true);

defineProps ({
  variant: {
    type: String,
    default: "home"
  },
  mobileProfile: {
    type: Boolean,
    default: false,
  }
});


</script>

<style scoped>
@import "@/style.css";

nav {
  @apply fixed w-full top-0 h-20 lg:h-40
}
button {
  @apply cursor-pointer
}
.s-home {
  @apply max-h-20 lg:max-h-40
}
.s-nav {
  @apply max-h-20
}
</style>
