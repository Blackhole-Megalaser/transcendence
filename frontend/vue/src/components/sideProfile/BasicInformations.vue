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
      <Button 
        variant="secondary" 
        side="left"
        @click="reAuth"
      >Change user</Button>
    </div>
    <div class="h-10 w-full xs:w-1/2 flex-center mt-2 xs:mt-0">
      <Button 
        variant="secondary" 
        side="right"
        @click="logout(true)"
      >Log out</Button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { storeToRefs }          from 'pinia';
import { useUserStore }         from '@storage';
import { getCookie }            from '@shared';

import defaultCat from '@assets/default_cat.png';
import Button     from '@components/Button.vue';

const userStore     = useUserStore();
const { userInfos } = storeToRefs(userStore);
const randomName    = "Stranger";
const username      = ref(userInfos.value?.username ?? randomName);
const profilePic    = ref(userInfos.value?.profile_image ?? defaultCat);

const reAuth  = async () => {
  const currentURI  = window.location.href.slice(window.location.origin.length).replace('?', '&');
  const URI         = `/login${currentURI !== '/' ? `?next=${currentURI}` : ''}`
  
  const isLogedOut  = await logout(false);
  if (isLogedOut)
    window.location.href = URI;
}

const logout  = async (reload) => {
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
    userStore.clear();
    if (reload) 
      window.location.reload();
    else
      return true;
  }
  catch (error) {
    console.error(error.message);
    return false;
  }
}
</script>

<style>
@import "@/style.css";

hr {
  @apply h-px border-sidebar-border my-6;
}
</style>
