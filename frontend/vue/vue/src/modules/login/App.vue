<template>
  <navBar
    @changeStatus="toggleSideBar"
    class="z-60"
    @showProfile="toggleSideProfile"
    :mobileProfile="MaskNavIcons"
    :isLogin="true"
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
    <section class="text-text-main h-full w-full flex-center flex-col">
      <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 xs:rounded-4xl shadow-xl">
        <h2 class="text-title text-4xl">
          Log In
        </h2>
        <div class="flex-center flex-col">
          <form action="post" class="flex flex-col">
            <div>
              <input type="text" class="informations" placeholder="Enter your Username">
            </div>
            <div>
              <input type="text" class="informations" placeholder="Enter your Password">
            </div>
            <div class="flex-center h-10 w-18 self-center">
              <input type="submit" class="px-4 py-1 rounded-full mt-1 input" value="Send">
            </div>
          </form>
        </div>
        <p class="text-sm text-sidebar-text-1">Don't have an account yet ?<a href="signup.html" class="underline"> Sign Up !</a></p>
      </div>
    </section>
  </main>
</template>


<script setup>
import { useThemeStore } from '@/storage/theme.js';
import { useBreakpoints } from '@vueuse/core';
import { ref, onMounted, onUnmounted, computed } from 'vue';

import Button from '@/components/Button.vue';
import NavBar from '@/components/NavBar.vue';
import SideBar from '@/components/SideBar.vue';
import SideProfile from '@/components/SideProfile.vue';

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
  if (ismobile.value) { console.log("true") ;return true; }
  else { console.log('false');   return false; }
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
.informations {
  @apply my-1 py-1 px-3 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active
}
.input {
  @apply shadow-button-2-normal;
  background-color: var(--color-button-2-normal);
  color: var(--color-text-button-2);
}
.input:hover {
  background-color: var(--color-button-2-hover);
}
.input:active {
  @apply duration-100 px-3.5 py-0.5;
  background-color: var(--);
}
.input:disabled {
  background-color: var(--color-button-2-disable);
}
</style>