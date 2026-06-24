import { computed, ref }  from "vue";
import { defineStore }    from "pinia";
import { fetchUserInfos } from "@shared";
import { getCookie }      from '@shared';

export const useUserStore = defineStore('user', () => {
  const STORAGE_KEY     ='user_infos_cache';
  const userInfos       = ref(JSON.parse(sessionStorage.getItem(STORAGE_KEY)) ?? null);
  const getLoggedStatus = computed(() => !!userInfos.value);
  const getProfilePic   = computed(() => userInfos.value ? userInfos.value.profile_image : null);

  function set(infos) {
    userInfos.value = infos;
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(infos));
  }

  function clear() {
    userInfos.value = null;
    sessionStorage.removeItem(STORAGE_KEY);
  }

  async function fetchInfos() {
    const infos = await fetchUserInfos();
    if (infos.status === 'ok')                    set(infos.data);
    else if (infos.status === 'unauthenticated')  clear()
    return(infos);
  }

  async function initUserInfos() {
    // if (userInfos.value) return userInfos.value;
    const infos = await fetchInfos();
    return infos.status === 'ok' ? infos.data : null;
  }

  return {
    set,
    clear,
    fetchInfos,
    initUserInfos,
    getLoggedStatus,
    getProfilePic,
    userInfos
  }
})
