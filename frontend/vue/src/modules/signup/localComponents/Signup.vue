<template>
  <section class="text-text-main h-full w-full flex-center gap-4 sm:px-6">
    <div
      class="absolute w-full top-20 p-4 bg-bg-main shadow-md z-40 transition duration-300"
      :class="OpenInfoBar && ismobile ? 'translate-y-0' : '-translate-y-400'"
    >
      <informations :password-check="Password"/>
    </div>
    <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 sm:rounded-4xl shadow-xl">
      <h2 class="text-title text-4xl">
        Sign Up
      </h2>
      <div class="flex-center flex-col">
        <form  @submit.prevent="submit" class="flex flex-col">
          <div class="flex">
            <Input
              v-model="Username"
              :input-validate="validateUser"
              p-holder="Enter your Username"
              input-type="text"
            />
          </div>
          <div class="flex">
            <Input
              v-model="Email"
              :input-validate="validateEmail"
              p-holder="Enter your Email"
              input-type="text"
            />
          </div>
          <div class="flex">
            <Input 
              v-model="Password" 
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
              v-model="PasswordRepeat"
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
              :class="validateForm ? 'cursor-pointer' : ''"
              :disabled="!validateForm"
            >
            <div class="size-4">
            </div>
          </div>
        </form>
      </div>
      <p class="text-sm text-sidebar-text-1">Already have an account ?<a :href="`login?next=${nextPage()}`" class="underline"> Log in !</a></p>
    </div>
    <aside 
      v-if="!ismobile"
      class="hidden sm:block bg-navbar rounded-4xl shadow-xl transition-all duration-300 transform"
      :class="OpenInfoBox 
        ? 'max-w-80 p-6 opacity-100 translate-x-0 max-h-96 rotate-360' 
        : 'max-w-0 p-0 opacity-0 -translate-x-10 pointer-events-none max-h-0 -rotate-360'
      "
    >
      <informations :password-check="Password"/>
    </aside>
  </section>
</template>

<script setup>
import { ref, computed }  from 'vue'
import { useBreakpoints } from '@vueuse/core';
import { getCookie }      from '@shared';
import forbiddenUsername  from '@shared/forbiddenUsernames.json'
import mostUsedPasswords  from '@shared/1000_mostUsedPasswords.json'
import Input              from './Input.vue';    
import informations       from './informations.vue'

import interogation       from '@assets/interrogation.svg'

const Email           = ref("");
const Username        = ref("");
const Password        = ref("");
const PasswordRepeat  = ref("");
const apiError        = ref("");
const OpenInfoBar     = ref(false);
const OpenInfoBox     = ref(false);
const nextPage  = () => { 
  const nextURL = new URLSearchParams(window.location.search).get('next');
  return nextURL ? nextURL : '/';
}

const breakpoints = useBreakpoints({ sm: 640 });
const ismobile    = breakpoints.smaller("sm");

const validateForm    = computed(() => {
  if (validatePass.value && validatePassRep.value && validateEmail.value && validateUser.value) { return true }
  else { return false }
})

const isMostUsedPassword  = computed(() => mostUsedPasswords.includes(Password.value.toLowerCase()))
const hasUppercase        = computed(() => /[A-Z]/.test(Password.value))
const hasNumber           = computed(() => /[0-9]/.test(Password.value))
const isLongEnough        = computed(() => Password.value.trim().length >= 8)

const validatePass        = computed(() => {
  if (isMostUsedPassword.value) { return false }
  if (!isLongEnough.value)      { return false }
  if (!hasUppercase.value)      { return false }
  if (!hasNumber.value)         { return false }
  return true
})

const passwordStatus  = computed(() => {
  return {
    isValidUppercase:         hasUppercase.value,
    isValidNumber:            hasNumber.value,
    isValidLength:            isLongEnough.value,
    isValidMostUsedPassword:  isMostUsedPassword.value
  }
})

const validatePassRep = computed(() => {
  if (Password.value === PasswordRepeat.value) { return true }
  else { return false }
})

const validateUser    = computed(() => {
  let lowerCaseUsername = Username.value.toLowerCase();

  if (forbiddenUsername.usernames.includes(lowerCaseUsername))                              { return false }
  else if (forbiddenUsername.prefixes.some(prefix => lowerCaseUsername.startsWith(prefix))) { return false }
  else if (forbiddenUsername.suffixes.some(suffix => lowerCaseUsername.endsWith(suffix)))   { return false }
  else if (forbiddenUsername.includes.some(word => lowerCaseUsername.includes(word)))       { return false }
  else if (!/[a-z]/.test(lowerCaseUsername))                                                { return false } // si aucuns characteres alphabetiques ne sont trouvers return false 
  else if (Username.value.length < 3)                                                       { return false }
  else                                                                                      { return true  }
})

const validateEmail   = computed(() => {
  const cleanEmail      = Email.value ? Email.value.trim() : "";

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

const submit    = async () => {
  apiError.value = '';
  try {
    const response  = await fetch('/api/users/signup/', {
      
      method: 'POST',
      body: JSON.stringify({
        username:               Username.value, 
        email:                  Email.value,
        password:               Password.value,
        password_confirmation:  PasswordRepeat.value
      }),
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type': 'application/json'
      }
    });
    if (!response.ok) {
      apiError.value  = await response.json();
      console.log(apiError.value.detail);
      throw new Error(`Wrong informations inserted: ${response.status}`)
    }
    window.location.href  = nextPage();
  }
  catch (error) {
    console.error("error catched :", error);
  }
}
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
