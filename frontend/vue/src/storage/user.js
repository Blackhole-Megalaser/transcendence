import { computed, defineAsyncComponent, ref }  from "vue";
import { defineStore }                          from "pinia";
import { fetchUserInfos, fetchFriendlist }         from "@shared";

export const useUserStore = defineStore('user', () => {
  const STORAGE_KEY     ='user_infos_cache';
  const userInfos       = ref(JSON.parse(sessionStorage.getItem(STORAGE_KEY)) ?? null);
  const getLoggedStatus = computed(() => !!userInfos.value);
  const getProfilePic   = computed(() => userInfos.value ? userInfos.value.profile_image : null);
  
    function set(infos) {
      userInfos.value = infos;
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(infos));
    }

  function changeEmail(newEmail) {
    userInfos.value.email = newEmail;
    set(userInfos.value);
  }

  function changeProfilePic(newProfilePic) {
    userInfos.value.profile_image = newProfilePic;
    set(userInfos.value);
  }

  function clear() {
    userInfos.value = null;
    sessionStorage.removeItem(STORAGE_KEY);
  }

  async function updateFriendlist() {
      const friendlist  = await fetchFriendlist();
      if (userInfos.value) {
        const data = { ...userInfos.value };
        data["friendlist"] = friendlist;
        set(data);
      }
  }
  
  function removeFriend(username) {
    if (userInfos.value) {
      userInfos.value.friendlist = userInfos.value.friendlist.filter((f) => f.username !== username);
      set(userInfos.value);
    }
  }

  async function fetchInfos() {
    const infos       = await fetchUserInfos();
    if (infos.status === 'ok') {
      const friendlist  = await fetchFriendlist();
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
    fetchInfos,
    changeEmail,
    removeFriend,
    initUserInfos,
    updateFriendlist,
    changeProfilePic,
    getLoggedStatus,
    getProfilePic,
    userInfos
  }
})
