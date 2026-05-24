<template>
  <section class="text-text-main h-full w-full flex-center flex-col">
    <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 xs:rounded-4xl shadow-xl">
      <h2 class="text-title text-4xl">
        Sign Up
      </h2>
      <div class="flex-center flex-col">
        <form action="post" class="flex flex-col">
          <div class="flex">
            <div class="size-4"/>
            <input 
              type="text" 
              class="informations" 
              placeholder="Enter your Username"
              v-model="username" 
            >
            <div class="size-4">
            </div>
          </div>
          <div class="flex">
            <div class="size-4"/>
            <input 
              type="text" 
              class="informations" 
              placeholder="Enter your Email"
              v-model="email"
            >
            <div class="size-4">
            </div>
          </div>
          <div class="flex">
            <div class="size-4"/>
            <input 
              type="password" 
              class="informations" 
              placeholder="Enter your Password"
              v-model="password"
            >
            <div class="size-4">
            </div>
          </div>
          <div class="flex">
            <div class="size-4"/>
            <input 
              type="password" 
              class="informations" 
              placeholder="Repeat your Password"
              v-model="passwordRepeat"
            >
            <div class="size-4">
            </div>
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
  </section>
</template>

<script setup>
import { ref, computed }  from 'vue'
import forbiddenUsername  from '@shared/forbiddenUsernames.json'

const email           = ref("");
const username        = ref("");
const password        = ref("");
const passwordRepeat  = ref("");


const validateForm    = computed(() => {
  if (validatePass.value && validatePassRep.value && validateEmail.value && validateUser.value) { return true }
  else { return false }
})

const validatePass    = computed(() => {
  if (password.length < 8) { return false }
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
    pour les nerds de regex ! /^(?!.*\.{2})[a-z0-9!#$%&'*+/=?^_`{|}~-]+$/i xD 
    ce regex autorise tous les characteres alphanumeriques et !#$%&'*+/=?^_-`{|}~
    et interdit d'avoir de points au debut, a la fin et deux points de suite 

    -> de base la RFC 5322 autorise tous les characteres imprimables ci dessus 
    mais gmail a une vision beaucoup plus strict de la chose et du coup autorise
    uniquement les characteres alpha numeriques. 
  */

  // Verification de la partie locale
  if (localPart.length < 1 || localPart.length > 64) { return false }
  if (/\.{2}/.test(localPart)) { return false } // interdit la suite de deux points ".."
  if (localPart.startsWith(".") || localPart.endsWith(".")) { return false }
  if (!/^[a-z0-9-._]+$/i.test(localPart)) { return false } // regarde si tous les characteres de la chaine sont valides (alpha numeriques)

  // Verification de la partie domaine
  const domainlength = domainPart.length;
  if (domainlength < 3 || domainlength > 253) { return false }
  if (domainPart.startsWith(".") || domainPart.endsWith(".")) { return false }
  if ((domainPart.match(/\./g) || []).length < 1 ) { return false }
  return true
})
</script>

<style>
@import '@/style.css';

.informations {
  @apply my-1 py-1 px-3 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active
}
.input {
  @apply shadow-button-2-normal;
  background-color: var(--color-button-2-normal);
  color: var(--color-text-button-2);
}
.input:hover {
  background-color: var(--color-button-2-hover);
}
.input:active {
  @apply duration-100 px-3.5 py-0.5;
  background-color: var(--);
}
.input:disabled {
  background-color: var(--color-button-2-disable);
}
</style>