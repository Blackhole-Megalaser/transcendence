<template>
  <BasePage>
    <SelectChat
      @general="changeChannel('general')"
      @naughty="changeChannel('naughtyCatHideout')"
      @cute="changeChannel('cutieCardboardBox')"
      class="fixed z-15 transition-transform duration-200"
      :class="openRoomSelection ? 'translate-x-0' : '-translate-x-300'"
    />
    <section 
      :class="openRoomSelection ? 'pl-72 xl:pl-80' : 'pl-0'"
      class="z-10 transition-transform duration-200"
    >
      <div class="w-full flex justify-between px-4 items-center bg-navbar shadow-sm">
        <component
          :is="menu"
          class="stroke-navbar-menu size-10 cursor-pointer"
          @click="openRoomSelection = !openRoomSelection"
        />
        <h2 class="text-title h-8 text-xl font-bold my-4">{{ formatChanName(currentChannel) }}</h2>
        <div class="size=10"></div>
      </div>
      <div class="h-[calc(100dvh-160px)]">
        <Chat
          initialRoomName="general"
          v-if="currentChannel === 'general'" 
        />
        <Chat
          initialRoomName="naughty_cat_hideout"
          v-else-if="currentChannel === 'naughtyCatHideout'" 
        />
        <Chat
          initialRoomName="cutie_cardboard_box"
          v-else-if="currentChannel === 'cutieCardboardBox'" 
        />
      </div>
    </section>
  </BasePage>
</template>

<script setup>
import { ref, onMounted, onUnmounted }  from 'vue';
import menu                             from '@assets/menu-chat.svg';

const openRoomSelection = ref(false);
const existingChannels  = ['general', 'naughtyCatHideout', 'cutieCardboardBox'];
const currentChannel    = ref('general');

const formatChanName  = (str) => {
  const lowerCaseWithSpaces = str.replace(/([A-Z])/g, ' $1').toLowerCase().trim();
  return lowerCaseWithSpaces.charAt(0).toUpperCase() + lowerCaseWithSpaces.slice(1); 
}

const getChannelFromUrl = () => {
  const URLParams = new URLSearchParams(window.location.search);
  const room      = URLParams.get('room');
  if (!room) {
    const newURL = `${window.location.pathname}?room=general`;
    window.history.pushState({ path: newURL }, '', newURL )
    currentChannel.value = 'general';
    return ;
  }
  else if (!existingChannels.find((chan) => chan === room)) {
    window.location.href = '/error_404';
    return ;
  }
  else {
    currentChannel.value = room;
  }
  document.title = `Chat - ${currentChannel.value}`;
}

const changeChannel   = (channelName) => {
  if (currentChannel === channelName) return;
  const newURL = `${window.location.pathname}?room=${channelName}`;
  currentChannel.value = channelName;
  window.history.pushState({ path: newURL }, formatChanName(currentChannel.value), newURL)
}

onMounted(() => {
  getChannelFromUrl();
  window.addEventListener('popstate', getChannelFromUrl());
})
onUnmounted(() => {
  window.removeEventListener('popstate', getChannelFromUrl());
})
</script>

<style scoped>

</style>
