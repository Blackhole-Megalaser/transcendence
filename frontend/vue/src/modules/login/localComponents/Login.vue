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
          <div class="flex-center h-10 w-18 self-center">
            <p class="text-red-600">{{ apiError }}</p>
            <input 
              type="submit" 
              class="input"
              value="Submit"
              :disabled="Username === '' || Password === ''"
            >
          </div>
        </form>
      </div>
      <p class="text-sm text-sidebar-text-1">Don't have an account yet ?<a href="signup" class="underline"> Sign Up !</a></p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed }  from 'vue';
import { getCookie }      from '@shared/cookieGetter';
import HideableInput      from "@components/HideableInput.vue";

const Username  = ref('');
const Password  = ref('');
const Error     = ref('');

const submit    = async () => {
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
      apiError  = response.detail;
      throw new Error('Wrong informations inserted: ', response.status);
    }
    console.log('done');
    window.location.href  = '/';
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
