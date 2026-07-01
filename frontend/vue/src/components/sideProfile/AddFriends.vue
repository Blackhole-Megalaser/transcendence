<template>
  <div class="flex flex-col gap-4">
    <h2 class="w-full text-center text-title text-3xl font-bold">Add a new friend</h2>
    <form @submit.prevent="submit" class="relative">
      <input 
        type="text" 
        class="informations w-full text-text-main/70"
        v-model="model"
        placeholder="Ex: Baguette42"
      >
      <div class="absolute inset-y-2 right-1 w-18">
        <input
          type="submit"
          class="input flex-center"
          value="Send"
          :disabled="model === ''"
        >
      </div>
    </form>
  </div>
</template>

<script setup>
const model = defineModel();

const sendRequest = async () => {
  try {
    const response  = await {
      
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
  @apply px-4 py-1 shadow-button-1-normal bg-button-1-normal text-text-button-1 hover:bg-button-1-hover disabled:bg-button-1-disable rounded-full mt-1 cursor-pointer;
}
.input:active {
  @apply duration-100 px-3.5 py-0.5;
}
.informations {
  @apply my-2 py-2 pl-4 pr-21 border border-input-text rounded-full bg-input-bg focus:bg-input-bg-active focus:outline-none focus:ring-2 focus:ring-title
}
</style>
