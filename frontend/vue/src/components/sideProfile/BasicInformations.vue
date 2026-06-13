<template>
  <div class="w-full flex-center flex-col">
    <img 
      :src='profilePic' alt="profile picture" 
      class="size-20 rounded-full"
    >
    <h2 class="mt-6 text-center font-bold text-2xl text-title">
      Hello
      <br class="xs:hidden"> {{ username }} !</h2>
  </div>
  <hr>
  <div class="flex flex-col gap-2 my-2">
    <a href="profile" class="h-10 flex-center">
      <Button>See profile page</Button>
    </a>
  </div>
  <div class="flex-center flex-col xs:flex-row">
    <div class="h-10 w-full xs:w-1/2 flex-center">
      <Button variant="secondary" side="left">Change user</Button>
    </div>
    <div class="h-10 w-full xs:w-1/2 flex-center mt-2 xs:mt-0">
      <Button 
        variant="secondary" 
        side="right"
        @click="logout"
      >Log out</Button>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, ref, watch } from 'vue';
import { getCookie }                    from '@shared';
import defaultCat                       from '@assets/default_cat.png';
import Button                           from '@components/Button.vue';

const userInfos       = inject('userInfos', ref(null));
const randomName      = "Stranger";
const username        = userInfos.value ? userInfos.value.username : randomName;
const profilePic      = userInfos.value ? userInfos.value.profile_image : defaultCat;

const logout  = async () => {
  try {
    const response  = await fetch('/api/users/logout/', {
      method: "POST",
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type': 'application/json'
      }
    })
    if (!response.ok)
      throw new Error(`Couldn't disconnect: ${response.status}`);
    window.location.reload();
  }
  catch (error) {
    console.error(error.message);
  }
}
</script>

<style>
@import "@/style.css";

hr {
  @apply h-px border-sidebar-border my-6;
}
</style>
