<template>
  <section class="text-text-main h-full w-full flex-center flex-col">
    <div class="flex items-center justify-evenly flex-col bg-navbar w-full h-full sm:w-96 sm:h-96 xs:rounded-4xl shadow-xl">
      <h2 class="text-title text-4xl">
        Log In
      </h2>
      <div class="flex-center flex-col">
        <form action="post" class="flex flex-col">
          <div>
            <input type="text" class="informations" placeholder="Enter your Username">
          </div>
          <div>
            <input type="text" class="informations" placeholder="Enter your Password">
          </div>
          <div class="flex-center h-10 w-18 self-center">
            <input type="submit" class="px-4 py-1 rounded-full mt-1 input" value="Send">
          </div>
        </form>
      </div>
      <p class="text-sm text-sidebar-text-1">Don't have an account yet ?<a href="signup" class="underline"> Sign Up !</a></p>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
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