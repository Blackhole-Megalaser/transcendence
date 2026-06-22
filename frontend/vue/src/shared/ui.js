import {
  ref,
  onMounted,
  onUnmounted,
  computed
} from 'vue';
import { useThemeStore }          from '@storage';
import { hasOwn, useBreakpoints } from '@vueuse/core';

export function useUi() {
  const breakpoints = useBreakpoints({sm: 640 });
  const ismobile = breakpoints.smaller("sm");

  const showSideBar = ref(false);
  const showProfile = ref(false);

  function closeSideBar() {
    if (showSideBar.value) showSideBar.value = false;
  }
  function closeProfile() {
    if (showProfile.value) showProfile.value = false;
  }
  const MaskNavIcons = computed (() => {
    if (ismobile.value && showProfile.value) { return true; }
    else { return false; }
  });

  function toggleSideBar() {
    if (!ismobile.value || (ismobile.value && !showProfile.value)) {
      showSideBar.value = !showSideBar.value;
    }
  }
  function toggleSideProfile() {
    if (!ismobile.value) {
      showProfile.value = !showProfile.value;
      return ;
    }
    else if (showSideBar.value) { showSideBar.value = false; }
    showProfile.value = !showProfile.value;
  }
  const handleKeyPress = (event) => {
    if (event.key === "Escape") {
      if (showProfile) {
        closeProfile();
      }
    }
  };
  onMounted(() => {
    window.addEventListener("keydown", handleKeyPress);
  });
  onUnmounted(() => {
    window.removeEventListener("keydown", handleKeyPress);
  });

  return {
    ismobile,
    showSideBar,
    showProfile,
    MaskNavIcons,
    toggleSideBar,
    toggleSideProfile,
    closeProfile,
    closeSideBar
  };
}
