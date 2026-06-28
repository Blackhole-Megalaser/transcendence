<template>
  <nav class="flex justify-center relative">
    <div
      class="flex items-center w-full h-20 bg-navbar border-b
        border-navbar-border px-3 sm:px-6 shadow-md"
    >
      <div class="flex flex-none justify-start w-1/5 sm:w-1/4 xl:w-1/3">
        <button v-if="!mobileProfile && !isLogin" class="flex-center" type="button" @click="$emit('changeStatus')">
          <component :is="currentPaw" class="fill-navbar-menu size-12" />
        </button>
        <div v-else-if="!mobileProfile && isLogin">
          <div class="hidden lg:flex">
            <ThemeButton />
          </div>
          <div class="flex lg:hidden">
            <ThemeToggle />
          </div>
        </div>
      </div>
      <div class="h-20 flex flex-1 justify-center items-center sm:items-start">
        <a href="/" class="cursor-pointer select-none" aria-label="back to home">
          <img
            :src="themeIndex === 0 ? ft_cat : ft_mean" alt="LOGO"
            :class="`s-${variant}`"
          >
        </a>
      </div>
      <div class="flex flex-none justify-end w-1/5 sm:w-1/4 xl:w-1/3 items-center">
        <div v-if="!mobileProfile && !isLogin" class="flex gap-5 lg:gap-10 ">
          <div class="hidden lg:flex">
            <ThemeButton />
          </div>
          <div class="hidden sm:max-lg:flex">
            <ThemeToggle />
          </div>
          <div class="flex items-center justify-end">
            <ProfileButton
              v-if="getLoggedStatus"
              class="flex"
              @click="$emit('showProfile')"
            />
            <div v-else class="flex">
              <a :href="`login${URI}`" class="h-10 sm:w-28 flex-center">
                <ButtonLogIn>
                  Log in
                </ButtonLogIn>
              </a>
              <a :href="`signup${URI}`" class="h-10 sm:w-32 hidden xl:flex justify-center items-center">
                <ButtonLogIn>
                  Sign Up
                </ButtonLogIn>
              </a>
            </div>

          </div>
        </div>
        <div v-else>
          <div v-if="isLogin">
            <button class="size-10 flex-center">
              <a :href="nextPage()">
                <component :is=cross alt="close window" class="size-8 fill-exit-cross" />
              </a>
            </button>
          </div>
          <div v-else>
            <button @click="$emit('showProfile')" class="size-10 flex-center">
              <component :is=cross alt="close window" class="size-8 fill-exit-cross" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import { storeToRefs }                  from 'pinia';

import { useThemeStore, useUserStore } 	from '@storage';

import ButtonLogIn 			from './ButtonLogIn.vue';
import ProfileButton 		from './ProfileButton.vue';
import ThemeButton 			from './ThemeButton.vue';
import ThemeToggle 			from './ThemeToggle.vue';

import cross 				  from '@assets/cross-svgrepo-com.svg'
import cute_paw 			from '@assets/cute_paw.svg?component';
import mean_paw 			from '@assets/mean_paw.svg?component';
import ft_cat 				from '@assets/ft_cat.png';
import ft_mean 				from '@assets/ft_cat-dark.png'

const theme               = useThemeStore();
const themeIndex          = computed (() => theme.getThemeIndex());
const currentPaw          = computed (() => themeIndex.value === 0 ? cute_paw : mean_paw);
const emit                = defineEmits(['changeStatus', 'showProfile', 'exitLogin']);
const userStore           = useUserStore();
const { getLoggedStatus } = storeToRefs(userStore);
const currentURI          = window.location.href.slice(window.location.origin.length).replace('?', '&');
const URI                 = currentURI !== '/' ? `?next=${currentURI}` : '';

const nextPage            = () => {
  let nextURL   = new URLSearchParams(window.location.search).get('next') ?? '/';
  let isSafeURL = true;
  if (!nextURL.startsWith('/')) nextURL   = '/' + nextURL;
  if (nextURL.length > 1)       isSafeURL = !nextURL.startsWith('//') && nextURL !== "/chat";
  return isSafeURL ? nextURL : '/';
}

defineProps ({
  variant: {
    type: String,
  },
  mobileProfile: {
    type: Boolean,
    default: false,
  },
  isLogin: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
@import "@/style.css";

nav {
  @apply fixed w-full top-0
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
