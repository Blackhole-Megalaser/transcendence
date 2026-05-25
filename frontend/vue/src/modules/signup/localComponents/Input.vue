<template>
  <div class="flex-center">
    <div class="size-9 flex-center">
      <component
        :is="status"
        :class="!inputValidate ? 'fill-red-600' : ''"
        class="size-4 flex items-center"
        v-if="!emptyModel"
      />
    </div>
    <input 
      :type="inputType" 
      :placeholder="pHolder"
      class="informations" 
      v-model="model"
    >
    <div class="size-9 flex-center">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBreakpoints } 	from '@vueuse/core';

import cross        from '@assets/wrong_cross.svg'
import check        from '@assets/check-mark.svg'

const model = defineModel();
const props = defineProps({
  inputValidate: {
    type: Boolean,
    default: false
  },
  informationComponent: {
    type: Boolean,
    default: false
  },
  pHolder: {
    type: String,
    default: "text"
  },
  inputType: String
});

const emptyModel  = computed(() => model.value.length < 1)
const status      = computed(() => props.inputValidate ? check : cross);
</script>

<style scoped>
@import '@/style.css';

.informations {
  @apply my-1 py-1 px-3 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active
}
</style>