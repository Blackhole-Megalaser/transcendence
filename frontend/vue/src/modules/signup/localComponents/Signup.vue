<template>
  <section class="text-text-main h-full w-full flex-center gap-4 sm:px-6">
    <div
      class="absolute w-full top-20 p-4 bg-bg-main shadow-md z-40 transition duration-300"
      :class="OpenInfoBar && ismobile ? 'translate-y-0' : '-translate-y-400'"
    >
      <informations />
    </div>
    <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 sm:rounded-4xl shadow-xl">
      <h2 class="text-title text-4xl">
        Sign Up
      </h2>
      <div class="flex-center flex-col">
        <form action="post" class="flex flex-col">
          <div class="flex">
            <Input
              v-model="username"
              :input-validate="validateUser"
              p-holder="Enter your Username"
              input-type="text"
            />
          </div>
          <div class="flex">
            <Input
              v-model="email"
              :input-validate="validateEmail"
              p-holder="Enter your Email"
              input-type="text"
            />
          </div>
          <div class="flex">
            <Input 
              v-model="password" 
              :input-validate="validatePass"
              p-holder="Enter your Password"
              input-type="password"
            >
              <component 
                v-if="ismobile"
                :is="interogation"
                class="size-4 flex items-center fill-sidebar-text-2 cursor-pointer"
                @click="OpenInfoBar = !OpenInfoBar"
              />
              <component 
                v-else-if="!ismobile"
                :is="interogation"
                class="size-4 flex items-center fill-sidebar-text-2 cursor-help"
                @click="OpenInfoBox = !OpenInfoBox"
              />
            </Input>
          </div>
          <div class="flex">
            <Input
              v-model="passwordRepeat"
              :input-validate="validatePassRep"
              p-holder="Repeat your Password"
              input-type="password"
            />
          </div>
          <div class="flex-center h-10 w-26 self-end">
            <div class="size-4"/>
            <input 
              type="submit" 
              value="Send"
              class="px-4 py-1 rounded-full mt-1 input"
              :disabled="!validateForm"
            >
            <div class="size-4">
            </div>
          </div>
        </form>
      </div>
      <p class="text-sm text-sidebar-text-1">Already have an account ?<a href="login" class="underline"> Log in !</a></p>
    </div>
    <aside 
      v-if="!ismobile"
      class="hidden sm:block bg-navbar rounded-4xl shadow-xl transition-all duration-300 transform"
      :class="OpenInfoBox 
        ? 'max-w-80 p-6 opacity-100 translate-x-0 max-h-96' 
        : 'max-w-0 p-0 opacity-0 -translate-x-10 pointer-events-none max-h-0'
      "
    >
      <informations />
    </aside>
  </section>
</template>

<script setup>
import { ref, computed }  from 'vue'
import { useBreakpoints } from '@vueuse/core';
import forbiddenUsername  from '@shared/forbiddenUsernames.json'
import Input              from './Input.vue';    
import informations       from './informations.vue'

import interogation       from '@assets/interrogation.svg'

const email           = ref("");
const username        = ref("");
const password        = ref("");
const passwordRepeat  = ref("");
const OpenInfoBar     = ref(false);
const OpenInfoBox     = ref(false);

const breakpoints = useBreakpoints({sm: 640 });
const ismobile    = breakpoints.smaller("sm");

const closeInfoBar    = computed(() => {
  if (OpenInfoBar.value) { OpenInfoBar.value = false }
})

const validateForm    = computed(() => {
  if (validatePass.value && validatePassRep.value && validateEmail.value && validateUser.value) { return true }
  else { return false }
})

const validatePass    = computed(() => {
  if (password.value.length < 8) { return false }
  if (!/(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).+/.test(password.value)) { return false }
  return true
})

const validatePassRep = computed(() => {
  if (password.value === passwordRepeat.value) { return true }
  else { return false }
})

const validateUser    = computed(() => {
  let lowerCaseUsername = username.value.toLowerCase();

  if (forbiddenUsername.usernames.includes(lowerCaseUsername)) { return false }
  else if (forbiddenUsername.prefixes.some(prefix => lowerCaseUsername.startsWith(prefix))) { return false }
  else if (forbiddenUsername.suffixes.some(suffix => lowerCaseUsername.endsWith(suffix))) { return false }
  else if (forbiddenUsername.includes.some(word => lowerCaseUsername.includes(word))) { return false }
  else if (!/[a-z]/.test(lowerCaseUsername)) { return false } // si aucuns characteres alphabetiques ne sont trouvers return false 
  else if (username.length < 3) { return false }
  else { return true }
})

const validateEmail   = computed(() => {
  const cleanEmail      = email.value ? email.value.trim() : "";

  if ((cleanEmail.match(/@/g) || []).length !== 1) { return false }
  
  const splitedAddress  = cleanEmail.split("@");
  const localPart       = splitedAddress[0];
  const domainPart      = splitedAddress[1];

  /* 
    For the regex nerds xD /^(?!.*\.{2})[a-z0-9!#$%&'*+/=?^_`{|}~-]+$/i
    This regex allows every alpha numericals chars and !#$%&'*+/=?^_-`{|}~
    and forbids string starting and ending with dots, and to have multiple 
    successives dots.

    -> the RFC 5322 allows almost every printable chars to be put in emails
    but because of anti fishing, scaming etc procedures, gmail only allows
    alpha numericals characters to be included in the local part
  */

  // Local part verification
  if (localPart.length < 1 || localPart.length > 64) { return false }
  if (/\.{2}/.test(localPart)) { return false } // forbid two or more successive dots ".."
  if (localPart.startsWith(".") || localPart.endsWith(".")) { return false }
  if (!/^[a-z0-9.]+$/i.test(localPart)) { return false } // Looks if every chars are valids (Alpha numerical + dots)

  // Domain part verification
  const domainlength = domainPart.length;
  if (domainlength < 3 || domainlength > 253) { return false }
  if (domainPart.startsWith(".") || domainPart.endsWith(".")) { return false }
  if ((domainPart.match(/\./g) || []).length < 1 ) { return false }
  return true
})
</script>

<style scoped>
@import '@/style.css';

.input {
  @apply shadow-button-2-normal bg-button-2-normal text-text-button-2 
    active:duration-100 px-3.5 py-0.5
  hover:bg-button-2-hover 
  disabled:bg-button-2-disable;
}
</style>