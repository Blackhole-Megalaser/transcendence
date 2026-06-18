<template>
  <div class="flex items-center gap-2 mb-3 w-full">
    <div class="flex h-7 w-7 items-center justify-center rounded-lg bg-navbar text-title">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
      </svg>
    </div>
    <h3 class="font-bold text-lg text-title flex items-center gap-1.5">
      Username Requirements <span class="font-medium">:3</span>
    </h3>
  </div>
  <p class="text-sm font-medium text-text-main/80 mb-4 leading-relaxed">
    To create your account, your username must have :
  </p>

  <ul class="space-y-2.5 text-sm font-semibold text-text-main text-justify">
    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="text-left flex-1">Between <span class="text-title font-bold">3</span> and <span class="text-title font-bold">12</span> characters</span>
      <component 
        class="size-4 right-0 shrink-0"
        :is="isValidLength ? check : cross"
        :class="isValidLength ? '' : 'fill-red-600'"
      />
    </li>

    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="text-left flex-1">At least one letter <span class="text-xs text-text-main/50 font-normal">(a-z)</span></span>
      <component 
        class="size-4 right-0 shrink-0"
        :is="hasLetter ? check : cross"
        :class="hasLetter ? '' : 'fill-red-600'"
      />
    </li>

    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="text-left flex-1">Must not contain any spaces</span>
      <component 
        class="size-4 right-0 shrink-0"
        :is="hasNoSpaces ? check : cross"
        :class="hasNoSpaces ? '' : 'fill-red-600'"
      />
    </li>

    <li class="flex items-center gap-2.5">
      <span class="size-1.5 rounded-full bg-title shrink-0"></span>
      <span class="text-left flex-1">Must be an available & valid username</span>
      <component 
        v-if="!emptyUsername"
        class="size-4 right-0 shrink-0"
        :is="isAllowedUsername ? check : cross"
        :class="isAllowedUsername ? '' : 'fill-red-600'"
      />
    </li>
  </ul>
</template>

<script setup>
import { computed } from 'vue'
import forbiddenUsername from '@shared/forbiddenUsernames.json'
import cross        from '@assets/wrong_cross.svg'
import check        from '@assets/check-mark.svg'

const props = defineProps({ 
  usernameCheck: {
    type: String,
    default: ''
  }
})

const lowerUsername = computed(() => props.usernameCheck.toLowerCase())
const emptyUsername = computed(() => props.usernameCheck.trim().length === 0)

const isValidLength = computed(() => props.usernameCheck.length >= 3 && props.usernameCheck.length <= 12)
const hasLetter     = computed(() => /[a-z]/.test(lowerUsername.value))
const hasNoSpaces   = computed(() => !props.usernameCheck.includes(' '))

const isAllowedUsername = computed(() => {
  const name = lowerUsername.value
  
  if (forbiddenUsername.usernames.includes(name)) return false
  if (forbiddenUsername.prefixes.some(prefix => name.startsWith(prefix))) return false
  if (forbiddenUsername.suffixes.some(suffix => name.endsWith(suffix))) return false
  if (forbiddenUsername.includes.some(word => name.includes(word))) return false
  
  return true
})
</script>

<style scoped>
/* Tu peux lier ton style.css ici si nécessaire, comme sur l'autre composant */
</style>
