<template>
  <BasePage>
    <SelectChat
      @general="changeChannel('general')"
      @naughty="changeChannel('naughtyCatHideout')"
      @cute="changeChannel('cutieCardboardBox')"
      class="fixed z-15"
    />
    <section class="pl-72 xl:pl-80 z-10">
      <div class="w-full flex justify-center py-6 bg-navbar shadow-sm">
        <h2 class="text-title text-xl font-bold">{{ formatChanName(currentChannel) }}</h2>
      </div>
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
    </section>
  </BasePage>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const existingChannels  = ['general', 'naughtyCatHideout', 'cutieCardboardBox']
const currentChannel    = ref('general')

const formatChanName  = (str) => {
  const lowerCaseWithSpaces = str.replace(/([A-Z])/g, ' $1').toLowerCase().trim();
  return lowerCaseWithSpaces.charAt(0).toUpperCase() + lowerCaseWithSpaces.slice(1); 
}

const changeChannel   = (channelName) => {
  
  if (currentChannel === channelName) return;

  if (!existingChannels.find((chan) => chan === channelName)) {
    window.location.href = '/error_404';
    return ;
  } 
  
  const newURL = `${window.location.pathname}?room=${channelName}`;
  currentChannel.value = channelName;
}
</script>

<style scoped>

</style>
