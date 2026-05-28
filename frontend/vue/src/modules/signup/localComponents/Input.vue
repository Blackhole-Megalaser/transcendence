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
    <hideable-input
      :type="inputType"
      :my-placeholder="pHolder"
      v-model="model"
      :isPassword="ispassword"
    />
    <div class="size-9 flex-center">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBreakpoints } 	from '@vueuse/core';
import HideableInput from '@components/HideableInput.vue';
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
const ispassword  = computed(() => props.inputType === "password")
</script>

<style scoped>
@import '@/style.css';

</style>
