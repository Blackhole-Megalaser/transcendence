<template>
  <navBar
    @changeStatus="toggleSideBar"
    class="z-60"
    @showProfile="toggleSideProfile"
    :mobileProfile="MaskNavIcons"
  />
  <SideProfile :open="showProfile" @keydown.=""/>
  <main class="fscreen" @click="closeProfile">
    <sideBar 
      :class="!showSideBar ? '-translate-x-60 rotate-360' : 'translate-x-0 -rotate-360'"
      class="transition duration-200 z-50"
    />
    <div
        :class="showSideBar ? 'undefined':'hidden'"
        class="transition duration-200 fscreen fixed z-49 bg-black/40"
        @click="closeSideBar"
    ></div>
    <TPlace class="z-40"/>
  </main>
</template>


<script setup>
import { useThemeStore } from '../../storage/theme.js';
import { useBreakpoints } from '@vueuse/core';
import { ref, onMounted, onUnmounted, computed } from 'vue';

import TPlace from './game/TPlace.vue';
import Button from '@components/Button.vue';
import NavBar from '@components/NavBar.vue';
import SideBar from '@components/SideBar.vue';
import SideProfile from '@components/SideProfile.vue';

const breakpoints = useBreakpoints({sm: 640 });{}
const ismobile = breakpoints.smaller("sm");
const showSideBar = ref(false);
const showProfile = ref(false);

function closeSideBar() {
  if (showSideBar.value) showSideBar.value = false;
}
function closeProfile() {
  if (showProfile.value) showProfile.value = false;
}
const MaskNavIcons = computed (() => {
  if (ismobile.value && showProfile.value) { console.log("hide") ;return false; }
  else { console.log('show');   return true; }
})

function toggleSideBar() {
  if (!ismobile.value) { showSideBar.value = !showSideBar.value; }
  else if (!showProfile.value) { showSideBar.value = true; }
}
function toggleSideProfile() {
  if (!ismobile.value) { 
    showProfile.value = !showProfile.value; 
    return ;
  }
  else if (showSideBar.value) { showSideBar.value = false; }
  showProfile.value = !showProfile.value;
}
const handleKeyPress = (event) => {
  if (event.key === "Escape") {
    if (showProfile) {
      closeProfile();
    }
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleKeyPress);
})
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyPress);
})

</script>

<style scoped>
@import '@/style.css';

.fscreen {
  @apply h-[calc(100dvh-5rem)] w-dvw
}

</style>

<!-- <template>
  <NavBar
    @changeStatus="showSideBar = !showSideBar"
    variant="nav"
    class="z-60"
  />

  <sideBar 
    :class="showSideBar === false ? '-translate-x-60 rotate-360' : 'translate-x-0 -rotate-360'"
    class="transition duration-200 z-50"
  />
  <main>
    <div
        :class="showSideBar ? 'undefined':'hidden'"
        class="transition duration-200 w-dvw h-dvh fixed z-49 bg-black/40"
        @click="closeSideBar"
    ></div>
    <TPlace class="z-40"/>
  </main>
</template>

<script setup>
import { ref } from 'vue';

import TPlace from './game/TPlace.vue';
import NavBar from '@components/NavBar.vue';
import SideBar from '@components/SideBar.vue';

const showSideBar = ref(false);

function closeSideBar() {
  if (showSideBar.value) showSideBar.value = false;
}

</script>

<style>
@import '../../style.css';

body {
  @apply bg-bg-main pt-20
}
</style> -->
