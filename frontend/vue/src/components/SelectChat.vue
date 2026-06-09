<template>
  <div class="w-full sm:w-72 xl:w-80 h-full bg-profile shadow">
    <div class="w-full pt-10 pb-4 flex-center">
      <h2 class="text-2xl text-title font-bold">Chat rooms</h2>
    </div>
    <hr>
    <ul>
      <li>
        <button @click="$emit('general')">General</button>
      </li>
      <li>
        <button @click="$emit('naughty')">Naughty Cat Hideout</button>
      </li>
      <li>
        <button @click="$emit('cute')">Cutie Cardboard Box</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed }  from 'vue';
import { useBreakpoints } from '@vueuse/core';


defineEmits(['general', 'naughty', 'cute']);

const props = defineProps({
  openSelect: {
    type: Boolean,
    default: false
  }
});

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
  @apply w-full text-text-main font-semibold text-lg px-6
}
button {
  @apply w-full hover:bg-button-2-normal px-6 py-2 flex items-center justify-start rounded-full
}
</style>
