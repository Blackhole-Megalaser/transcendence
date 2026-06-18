<template>
  <div class="flex items-center gap-2 mb-3 w-full">
    <div class="flex h-7 w-7 items-center justify-center rounded-lg bg-navbar text-title">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
      </svg>
    </div>
    <h3 class="font-bold text-lg text-title flex items-center gap-1.5">
      Password Requirements <span class="font-medium">:3</span>
    </h3>
  </div>
  <p class="text-sm font-medium text-text-main/80 mb-4 leading-relaxed">
    To ensure your account remains secure, your password must include :
  </p>

  <ul class="space-y-2.5 text-sm font-semibold text-text-main text-justify">
    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="w-86 sm:w-56">At least <span class="text-title font-bold">8</span> characters, and a maximum of <span class="text-title font-bold">40</span> characters</span>
      <component 
        class="size-4 right-0"
        :is="isValidLength ? check : cross"
        :class="isValidLength ? '' : 'fill-red-600'"
      />
    </li>
    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="w-86 sm:w-56">One uppercase letter <span class="text-xs text-text-main/50 font-normal">(A-Z)</span></span>
      <component 
        class="size-4 right-0"
        :is="hasUppercase ? check : cross"
        :class="hasUppercase ? '' : 'fill-red-600'"
      />
    </li>
    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="w-86 sm:w-56">One number <span class="text-xs text-text-main/50 font-normal">(0-9)</span></span>
      <component 
        class="size-4 right-0"
        :is="hasNumber ? check : cross"
        :class="hasNumber ? '' : 'fill-red-600'"
      />
    </li>
    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="w-86 sm:w-56">Must not be in the top 1000 most used passwords </span>
      <component 
        v-if="!emptyPassword"
        class="size-4 right-0"
        :is="isMostUsedPassword ? cross : check"
        :class="isMostUsedPassword ? 'fill-red-600' : ''"
      />
    </li>
  </ul>
</template>

<script setup>
import { computed } from 'vue'
import mostUsedPasswords  from '@shared/1000_mostUsedPasswords.json'
import cross        from '@assets/wrong_cross.svg'
import check        from '@assets/check-mark.svg'

const props = defineProps({ 
  passwordCheck: {
    type: String,
    default: ''
  }
})
const isMostUsedPassword  = computed(() => mostUsedPasswords.includes(props.passwordCheck.toLowerCase()));
const hasUppercase        = computed(() => /[A-Z]/.test(props.passwordCheck));
const hasNumber           = computed(() => /[0-9]/.test(props.passwordCheck));
const isValidLength       = computed(() => props.passwordCheck.length >= 8 && props.passwordCheck.length <= 40 );
const emptyPassword       = computed(() => props.passwordCheck.trim().length === 0);
</script>

<style>
</style>
