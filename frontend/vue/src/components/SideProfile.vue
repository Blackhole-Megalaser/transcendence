<template>
  <dialog 
    ref="dialog"
  >
    <div class="w-full flex-center flex-col">
      <img 
        :src='ProfilePicture' alt="profile picture" 
        class="size-20 rounded-full"
      >
      <h2 class="mt-6 text-center font-bold text-2xl text-title">
        Hello
        <br class="xs:hidden"> {{ UserName }} !</h2>
    </div>
    <hr>
    <div class="flex flex-col gap-2 my-2">
      <div class="h-10 flex-center">
        <Button>See profile page</Button>
      </div>
      <div class="h-10 flex-center">
        <Button>See Friendlist</Button>
      </div>
    </div>
    <div class="flex-center flex-col xs:flex-row">
      <div class="h-10 w-full xs:w-1/2 flex-center">
        <Button variant="secondary" side="left">Change user</Button>
      </div>
      <div class="h-10 w-full xs:w-1/2 flex-center mt-2 xs:mt-0">
        <Button variant="secondary" side="right">Log out</Button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

import defaultcat from '../assets/default_cat.png';
import Button from './Button.vue';

const props = defineProps({open: Boolean});
const username = ref("");
const dialog = ref(null);
const profilePic = ref(null);
const randomName = "Stranger";

watch(() => props.open, (val) => {
  val ? dialog.value.show() : dialog.value.close()
})

// Futur getter par API


const ProfilePicture = computed (() => {
  return profilePic.value ?? defaultcat;
})

const UserName = computed (() => {
  return username.value || randomName
})

</script>

<style scoped>
@import "@/style.css";

dialog {
  @apply sm:m-2 w-full h-full z-70 sm:w-md sm:h-auto sm:rounded-4xl 
    shadow-md fixed left-auto p-12;
  background-color: var(--color-profile);
}
hr {
  @apply h-px border-navbar-border my-6;
}
</style>

