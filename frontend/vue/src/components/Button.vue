<template>
  <button
    :class="[`btn-base-${side}`,`btn-${variant}`]"
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
  },
  side: {
    type: [String, Object],
    default: "both"
  }
});

const emit = defineEmits(['changeStatus']);

</script>

<style scoped>
@import "@/style.css";

.btn-base-both {
  @apply px-6 py-2 w-full rounded-full font-bold transition-all duration-300 shadow-xs;
}
.btn-base-left {
  @apply px-6 py-2 w-full rounded-full xs:rounded-r-none font-bold transition-all duration-300 shadow-xs;
}
.btn-base-right {
  @apply px-6 py-2 w-full rounded-full xs:rounded-l-none font-bold transition-all duration-300 shadow-xs;
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
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-1-active);
}
.btn-primary:disabled {
  background-color: var(--color-button-1-disable);
}
.btn-secondary {
  @apply shadow-button-2-normal;
  background-color: var(--color-button-2-normal);
  color: var(--color-text-button-2);
}
.btn-secondary:hover {
  background-color: var(--color-button-2-hover);
}
.btn-secondary:active {
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-2-active);
}
.btn-secondary:disabled {
  background-color: var(--color-button-2-disable);
}
.btn-log-in {
  @apply shadow-button-1-normal;
  background-color: var(--color-button-1-normal);
  color: var(--color-text-button-1);
}
.btn-log-in:hover {
  background-color: var(--color-button-1-hover);
}
.btn-log-in:active {
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-1-active);
}

</style>
