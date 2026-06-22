<template>
  <div class="relative w-full h-auto">
    <input
      :type="isPassword ? inputType : 'text'"
      class="informations w-full"
      :class="isPassword ? 'pr-10' : 'pr-3'"
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
import { computed, ref, watch }  from "vue";
import visible            from "@assets/visible.svg"
import nonVisible         from "@assets/non-visible.svg"

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
  @apply my-1 py-1 pl-3 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active focus:outline-none focus:ring-2 focus:ring-title
}
</style>
