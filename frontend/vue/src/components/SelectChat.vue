<template>
  <div class="w-full sm:w-72 xl:w-80 h-full bg-profile shadow">
    <div class="w-full pt-10 pb-4 flex-center">
      <h2 class="text-2xl text-title font-bold">Chat rooms</h2>
    </div>
    <hr>
    <ul>
      <li>
        <a href="/chat/cat_hideout">Cat Hideout</a>
      </li>
      <li>
        <a href="/chat/cardboard_box">Cardboard Box</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed }  from 'vue';
import { useBreakpoints } from '@vueuse/core';

const props = defineProps({
  openSelect: {
    type: Boolean,
    default: false
  }
})

const breakpoints   = useBreakpoints({ xl: 1280 });
const isSmallScreen = breakpoints.smaller("xl");
const isOpen        = ref("yes");

</script>

<style scoped>
@import "@/style.css";

hr {
  @apply h-px border-sidebar-border my-6 mx-4;
}
li {
  @apply w-full text-text-main font-semibold text-lg flex items-center pl-12
}
a {
  @apply w-full hover:bg-button-2-normal px-4 py-2 rounded-full
}
</style>
