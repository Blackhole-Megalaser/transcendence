<template>
  <button 
    :class="['btn-base',`btn-${variant}`]"
    @click="$emit('changeStatus')"
  >
    <slot />
  </button>
</template>

<script setup>

defineProps ({
  variant: {
    type: String,
    default: "primary"
  }
});

const emit = defineEmits(['changeStatus']);

</script>

<style scoped>
@import "@/style.css";

.btn-base {
  @apply px-2 py-1 sm:px-6 sm:py-2 rounded-full font-bold transition-all duration-300 shadow-xs;
}
.btn-primary {
  @apply shadow-button-1-normal;
  background-color: var(--color-button-1-normal);
  color: var(--color-text-button-1);
}
.btn-primary:hover {
  background-color: var(--color-button-1-hover);
}
.btn-primary:active {
  @apply duration-100 px-1.5 py-0.5 sm:px-5.5 sm:py-1.5;
  background-color: var(--color-button-1-active);
}


</style>