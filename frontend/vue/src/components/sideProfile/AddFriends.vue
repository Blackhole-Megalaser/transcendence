<template>
  <div class="flex flex-col gap-4">
    <h2 class="w-full text-center text-title text-3xl font-bold">Add a new friend</h2>
    <form @submit.prevent="sendRequest" class="relative">
      <input 
        type="text" 
        class="informations w-full text-text-main/70"
        v-model="model"
        placeholder="Ex: Baguette42"
      >
      <div class="absolute flex-center inset-y-2 right-1 w-18 h-10">
        <input
          type="submit"
          class="input"
          value="Send"
          :disabled="model === '' || !model"
        >
      </div>
      <div 
        class="text-center w-full" 
        :class="response.ok ? 'text-text-main' : 'text-red-600'"
        v-if="apiResponse"
      >
        <p>{{ apiResponse.detail }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref }        from 'vue';
import { getCookie }  from '@shared'

const model       = defineModel();
const apiResponse = ref(null);
const response    = ref(null);

const sendRequest = async () => {
  apiResponse.value = null; 
  try {
    response.value  = await fetch('/api/users/me/friends_request/', {
      method: 'POST',
      headers: { 
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-type': 'application/json'
       },
      body: JSON.stringify({
        action: 'send',
        username: model.value
      })
    })
    model.value = '';
    apiResponse.value = await response.value.json();
    if (!response.value.ok) {
      throw ("Friend request error: " + apiResponse.value.detail);  
    }
  }
  catch (e) {
    console.error(e);
  }
}
</script>

<style scoped>
@import '@/style.css';

.input {
  @apply px-4 py-1 shadow-button-1-normal bg-button-1-normal text-text-button-1 hover:bg-button-1-hover disabled:bg-button-1-disable rounded-full cursor-pointer;
}
.input:active {
  @apply duration-100 px-3.5 py-0.5;
}
.informations {
  @apply my-2 py-2 pl-4 pr-21 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active focus:outline-none focus:ring-2 focus:ring-title
}
</style>
