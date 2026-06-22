<template>
  <button
    :class="['btn-base',`btn-${variant}`]"
    @click="$emit('changeStatus')"
    type="button"
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
  @apply px-5 py-2 w-full rounded-full font-bold transition-all duration-300 cursor-pointer flex justify-start;
}
.btn-primary {
  color: var(--color-sidebar-text-1);
}
.btn-primary:hover {
  background-color: var(--color-button-sidebar-1-hover);
}
.btn-primary:active {
  @apply duration-100 px-5.5 py-1.5;
  background-color: var(--color-button-sidebar-1-active);
}
.btn-secondary {
  @apply hover:bg-button-sidebar-2-hover active:bg-button-sidebar-2-active
    text-sidebar-text-2

}
</style>
