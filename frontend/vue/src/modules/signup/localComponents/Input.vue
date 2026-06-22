<template>
  <div class="flex justify-center flex-col xl:py-1 w-full">
    <h3
      v-if="!isSmallScreen"
      class="font-bold text-text-main pl-9"
    >{{ pHolder }}:</h3>
    <div class="flex-center w-full">
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
        :my-placeholder="isSmallScreen ? pHolder : bigScreenPHolder"
        v-model="model"
        :isPassword="ispassword"
      />
      <div class="size-9 flex-center">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed }         from 'vue'
import { useBreakpoints } 	from '@vueuse/core';
import HideableInput        from '@components/HideableInput.vue';
import cross                from '@assets/wrong_cross.svg'
import check                from '@assets/check-mark.svg'

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
  bigScreenPHolder: {
    type: String,
    default: "text"
  },
  inputType: String
});

const emptyModel    = computed(() => model.value.length < 1)
const status        = computed(() => props.inputValidate ? check : cross);
const ispassword    = computed(() => props.inputType === "password")
const breakpoints   = useBreakpoints({ xl: 1280 });
const isSmallScreen = breakpoints.smaller("xl");
</script>

<style scoped>
@import '@/style.css';

</style>
