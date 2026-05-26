<template>
  <div class="relative w-full">
    <input 
      :type="isPassword ? inputType : 'text'" 
      class="informations w-full" 
      :placeholder="myPlaceholder"
      v-model="model"
    >
    <component 
      v-if="isPassword"
      :is="typeStatusImg" 
      @click="showPassword = !showPassword"
      class="size-8 absolute inset-y-1 right-0 flex justify-center items-center cursor-pointer pr-3 fill-text-button-2"
      />
  </div>
</template>

<script setup>
import visible from "@assets/visible.svg"
import nonVisible from "@assets/non-visible.svg"
import { computed, ref } from "vue";

const showPassword  = ref(false);
const inputType     = computed(() => showPassword.value ? "text" : "password");
const typeStatusImg = computed(() => showPassword.value ? visible : nonVisible);

const model = defineModel();
const props = defineProps({
  isPassword: {
    type: Boolean,
    default: false
  },
  myPlaceholder: {
    type: String,
    default: "Default Placeholder (change it)"
  }
});
</script>

<style scoped>
@import '@/style.css';

.informations {
  @apply my-1 py-1 px-3 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active
}
</style>
