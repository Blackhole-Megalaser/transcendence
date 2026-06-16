<template>
  <section class="text-text-main h-full w-full flex-center flex-col">
    <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 xs:rounded-4xl shadow-xl">
      <h2 class="text-title text-4xl">
        Log In
      </h2>
      <div class="flex-center flex-col">
        <form @submit.prevent="submit" class="flex flex-col">
          <HideableInput
            myPlaceholder="Enter your username"
            v-model="Username"
          />
          <HideableInput
            :isPassword="true"
            myPlaceholder="Enter your password"
            v-model="Password"
          />
          <div class="flex-center flex-col h-auto w-full self-center">
            <p class="text-red-600 text-sm py-2">{{ apiError.detail }}</p>
            <input 
              type="submit" 
              class="input flex-center"
              value="Submit"
              :disabled="Username === '' || Password === ''"
            >
          </div>
        </form>
      </div>
      <p class="text-sm text-sidebar-text-1">Don't have an account yet ?<a :href="`signup?next=${nextPage()}`" class="underline"> Sign Up !</a></p>
    </div>
  </section>
</template>

<script setup>
import { ref }        from 'vue';
import { getCookie }  from '@shared';
import HideableInput  from "@components/HideableInput.vue";

const Username  = ref('');
const Password  = ref('');
const apiError  = ref('');
const nextPage  = () => { 
  let nextURL   = new URLSearchParams(window.location.search).get('next') ?? '/';
  let isSafeURL = true;
  if (!nextURL.startsWith('/')) nextURL     = '/' + nextURL;
  if (nextURL.length > 1)       isSafeURL  = !nextURL.startsWith('//');
  return isSafeURL ? nextURL : '/';
}

const submit    = async () => {
  apiError.value = '';
  try {
    const response  = await fetch('/api/users/login/', {
      
      method: 'POST',
      body: JSON.stringify({
        username: Username.value, 
        password: Password.value
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
  }
}

</script>

<style scoped>
@import '@/style.css';

.input {
  @apply shadow-button-2-normal bg-button-2-normal text-text-button-2 hover:bg-button-2-hover disabled:bg-button-2-disable px-4 py-1 rounded-full mt-1 cursor-pointer;
}
.input:active {
  @apply duration-100 px-3.5 py-0.5;
}
</style>
