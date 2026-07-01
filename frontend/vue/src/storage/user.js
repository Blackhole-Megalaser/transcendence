import { computed, defineAsyncComponent, ref }  from "vue";
import { defineStore }                          from "pinia";
import { fetchUserInfos, fetchFriends }         from "@shared";

export const useUserStore = defineStore('user', () => {
  const STORAGE_KEY     ='user_infos_cache';
  const userInfos       = ref(JSON.parse(sessionStorage.getItem(STORAGE_KEY)) ?? null);
  const getLoggedStatus = computed(() => !!userInfos.value);
  const getProfilePic   = computed(() => userInfos.value ? userInfos.value.profile_image : null);
  
    function set(infos) {
      userInfos.value = infos;
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(infos));
    }

  function changeProfilePic(newProfilePic) {
    userInfos.value.profile_image = newProfilePic;
    set(userInfos.value)
  }

  function clear() {
    userInfos.value = null;
    sessionStorage.removeItem(STORAGE_KEY);
  }

  async function addFriend() {
      const friendlist  = await fetchFriends();
      infos.data["friendlist"] = friendlist;
      set(infos.data);
  }

  async function fetchInfos() {
    const infos       = await fetchUserInfos();
    if (infos.status === 'ok') {
      const friendlist  = await fetchFriends();
      infos.data["friendlist"] = friendlist;
      set(infos.data);
    }
    else if (infos.status === 'unauthenticated')  clear()
    return(infos);
  }

  async function initUserInfos() {
    const infos = await fetchInfos();
    return infos.status === 'ok' ? infos.data : null;
  }

  return {
    set,
    clear,
    addFriend,
    fetchInfos,
    initUserInfos,
    changeProfilePic,
    getLoggedStatus,
    getProfilePic,
    userInfos
  }
})
