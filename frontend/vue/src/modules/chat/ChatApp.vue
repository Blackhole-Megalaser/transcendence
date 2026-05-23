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
import { useUi } from '@shared'

const {
    ismobile,
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