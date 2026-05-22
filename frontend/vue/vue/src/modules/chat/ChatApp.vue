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
	<Chat/>
  </main>
</template>

<script setup>
import { useThemeStore }  from '@storage/theme.js';
import { useBreakpoints } from '@vueuse/core';
import { ref, onMounted, onUnmounted, computed } from 'vue';

import Button      from '@components/Button.vue';
import Chat        from '@components/Chat.vue';
import NavBar      from '@components/NavBar.vue';
import SideBar     from '@components/SideBar.vue';
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
@import "@/style.css";

.fscreen {
  @apply h-[calc(100dvh-5rem)] w-dvw
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  @apply bg-bg-main pt-20
}

</style>