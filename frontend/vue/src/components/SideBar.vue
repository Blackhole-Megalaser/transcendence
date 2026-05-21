<template>
  <div class="w-60 h-[calc(100svh-5rem)] bg-sidebar fixed top-20">
    <aside class="p-6 h-full w-full flex flex-col">
      <header class="flex-none">
        <div class="flex-center">
          <img 
            :src="!themeIndex ? cute_cat : mean_cat" 
            alt="mini logo"
            class="size-20"
          >
        </div>
        <hr>
      </header>
      <section class="flex-auto">
        <ul 
          class="flex flex-col text-red-500"
        >
          <li class="min-h-10 flex-col items-center">
            <ButtonSideBar
              @changeStatus="showGames = !showGames"
            >Games</ButtonSideBar>
            <div 
              :class="showGames === false ? 'hidden' : 'flex flex-col'"
              class="pl-6"
            >
              <ul 
                class="bg-button-sidebar-2-normal rounded-3xl"
              >
                <li>
                  <a href="skribbl.html">
                    <ButtonSideBar
                      variant="secondary"
                    >
                      skribbl.cat
                    </ButtonSideBar>
                  </a>
                </li>
                <li>
                  <a href="tplace.html">
                      <ButtonSideBar
                        variant="secondary"
                      >
                        tplace
                      </ButtonSideBar>
                    </a>
                </li>
              </ul>
            </div>
          </li>
          <li class="h-10 flex items-center">
            <a href="http://localhost:8000/chat" class="w-full">
              <ButtonSideBar>Chat rooms</ButtonSideBar>
            </a>
          </li>
          <li class="h-10 flex items-center">
            <ButtonSideBar>Friendlist</ButtonSideBar>
          </li>
        </ul>
      </section>
      <footer class="flex-none text-xs underline text-sidebar-footer">
        <hr>
        <a href="">Termes de Service</a>
        <br>
        <a href="">Politique de confidentialité</a>
      </footer>
    </aside>
  </div>
</template>

<script setup>
import { useThemeStore } from '../storage/theme.js';
import ThemeButton from './ThemeButton.vue';
import { computed, ref } from 'vue';
import ButtonSideBar from './ButtonSideBar.vue';
import mean_cat from '../assets/logo-dark-tr.png'
import cute_cat from '../assets/logo1-tr.png'

const theme = useThemeStore();
const themeIndex = computed (() => theme.getThemeIndex())
const showGames = ref(false);
const showFriendList = ref(false);

</script>

<style scoped>
@import "@/style.css";

hr {
  @apply h-px my-6 border-sidebar-border
}
</style>