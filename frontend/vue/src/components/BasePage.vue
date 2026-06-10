<template>
  <navBar
    @showProfile="toggleSideProfile"
    @changeStatus="toggleSideBar"
    class="z-60"
    :mobileProfile="MaskNavIcons"
    :isLogin="islogin"
    :variant="navBarVariant"
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
    <slot />
  </main>
</template>

<script setup>
import { useUi, Button, NavBar, SideBar, SideProfile } from '@shared'
import { computed } from 'vue';

const props = defineProps({
  islogin: {
    type: Boolean,
    default: false
  },
  navBarVariant: {
    type: String,
    default: 'home'
  }
})

const {
    showSideBar,
    showProfile,
    MaskNavIcons,
    toggleSideBar,
    toggleSideProfile,
    closeProfile,
    closeSideBar
} = useUi();
</script>

<style scoped>
@import "@/style.css";

</style>
