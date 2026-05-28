<template>
  <dialog ref="dialog">
    <div class="h-8 w-full flex-center gap-4">
      <button @click="bar = 0" class="size-6 cursor-pointer">1</button>
      <button @click="bar = 1" class="size-6 cursor-pointer">2</button>
      <button @click="bar = 2" class="size-6 cursor-pointer">3</button>
    </div>
    <hr>
    <BasicInformations v-if="selectWindow === 0"/>
    <Social v-else-if="selectWindow === 1"/>
    <Settings v-else/>
  </dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import BasicInformations        from './sideProfile/BasicInformations.vue';
import Social               from './sideProfile/Social.vue';
import Settings                 from './sideProfile/Settings.vue';

const props   = defineProps({open: Boolean});
const dialog  = ref(null);
const bar     = ref(0);

const selectWindow  = computed(() => bar.value === 0 ? 0 : (bar.value === 1 ? 1 : 2))

watch(() => props.open, (val) => {
  val ? dialog.value.show() : dialog.value.close()
})

// Futur getter par API
</script>

<style scoped>
@import "@/style.css";

dialog {
  @apply sm:m-2 w-full h-full z-70 sm:w-md sm:h-auto sm:rounded-4xl 
    shadow-md fixed left-auto p-12 pt-6;
  background-color: var(--color-profile);
}

hr {
  @apply h-px border-sidebar-border my-6;
}
</style>

