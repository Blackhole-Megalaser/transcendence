<template>
  <BasePage
    navBarVariant="nav"
  >
    <Skribbl />
  </BasePage>
</template>

<script setup>
import { 
  computed,
  onMounted,
  onUnmounted, 
  provide, 
  ref,
  watch 
} from 'vue';
import { fetchFriends }  from '@shared';
import { useThemeStore } from '@storage';
import scribblCatLogo    from '@assets/scribblcat.png';

const friendInfos = ref({ status: '', friends: [], pending_friend_requests: []});
let   timer       = null;
const theme       = useThemeStore();
const themeIndex  = computed(() => theme.getThemeIndex());
let originalNavbarLogo = null;
let navbarLogoFrameId = 0;

provide('FRIENDREQUESTS', friendInfos);

const getNavbarLogo = () => document.querySelector('nav a[aria-label="back to home"] img');

const setScribblNavbarLogo = () => {
  const logo = getNavbarLogo();

  if (!(logo instanceof HTMLImageElement)) return;
  if (!originalNavbarLogo) {
    originalNavbarLogo = {
      src: logo.src,
      alt: logo.alt,
    };
  }
  logo.src = scribblCatLogo;
  logo.alt = 'scribbl.cat';
}

const scheduleScribblNavbarLogo = () => {
  if (navbarLogoFrameId !== 0) {
    window.cancelAnimationFrame(navbarLogoFrameId);
  }
  navbarLogoFrameId = window.requestAnimationFrame(() => {
    navbarLogoFrameId = 0;
    setScribblNavbarLogo();
  });
}

const restoreNavbarLogo = () => {
  if (navbarLogoFrameId !== 0) {
    window.cancelAnimationFrame(navbarLogoFrameId);
    navbarLogoFrameId = 0;
  }

  const logo = getNavbarLogo();

  if (!(logo instanceof HTMLImageElement) || !originalNavbarLogo) return;
  logo.src = originalNavbarLogo.src;
  logo.alt = originalNavbarLogo.alt;
  originalNavbarLogo = null;
}

const refreshFriendRequest = async () => {
  const result = await fetchFriends();
  if (result.status === 'ok') {
    friendInfos.value = result;
  } else {
    friendInfos.value = {
      ...friendInfos.value,
      status: 'error'
    }
  }
}

onMounted(async () => {
  scheduleScribblNavbarLogo();
  await refreshFriendRequest();
  timer = setInterval( refreshFriendRequest, 5000);
})

onUnmounted(() => {
  restoreNavbarLogo();
  clearInterval(timer);
})

watch(themeIndex, scheduleScribblNavbarLogo, { flush: 'post' })
</script>

<style scoped>
</style>
