import { computed, ref }  from "vue";
import { defineStore }    from "pinia";
import { fetchUserInfos } from "@shared";

export const useUserStore = defineStore('user', () => {
  const CACHE_KEY       ='user_infos_cache';
  const userInfos       = ref(JSON.parse(sessionStorage.getItem(CACHE_KEY)) ?? null);
  const getUserInfos    = computed(() => userInfos.value);
  const getLoggedStatus = computed(() => userInfos.value ? true : false);
  const getProfilePic   = computed(() => userInfos.value ? userInfos.value.profile_image : null);

  function set(infos) {
    userInfos.value = infos;
    sessionStorage.setItem(CACHE_KEY, JSON.stringify(infos));
  }

  function clear() {
    userInfos.value = null;
    sessionStorage.removeItem(CACHE_KEY);
  }

  async function fetchInfos() {
    const infos = await fetchUserInfos();
    if (infos.status === 'ok')                    set(infos.data);
    else if (infos.status === 'unauthenticated')  clear()
    return(infos);
  }

  async function initUserInfos() {
    if (userInfos.value) return userInfos.value;
    const infos = await fetchInfos();
    return infos.status === 'ok' ? infos.data : null;
  }

  return {
    set,
    clear,
    fetchInfos,
    initUserInfos,
    getUserInfos,
    getLoggedStatus,
    getProfilePic
  }
})
