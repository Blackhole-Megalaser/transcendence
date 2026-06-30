<template>
  <section class="w-full flex-center flex-col gap-8 lg:gap-12 p-8 pt-12 md:max-xl:pb-0 lg:pt-24!">
    <div class="w-full grid grid-cols-1 md:grid-cols-2 items-center gap-4">
      <div class="flex-center flex-col gap-8">
        <div
          class="size-24 rounded-full bg-cover bg-center cursor-pointer"
          :style="{ backgroundImage: `url(${profilePic})` }"
          @click="$refs.fileInput.click()"
        />
        <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange">
        <div v-if="newImage" class="flex items-end justify-center gap-2">
          <p class="text-text-main/60 w-24 truncate">{{ newImageFile.name }}</p>
          <Button @click="changeProfilePicture()">Submit</Button>
        </div>
      </div>
      <div class="flex flex-col justify-center items-center gap-4">
        <div class="text-title text-4xl font-bold">{{ username }}</div>
        <p class="text-text-main/60">{{ email }}</p>
      </div>
    </div>
    <div class="w-full grid grid-cols-1 sm:grid-cols-3 gap-4" v-if="gameInfos">
      <div class="flex-center flex-col gap-2 p-6 rounded-2xl bg-surface">
        <div class="flex items-center gap-2">
          <img src="" alt="Nyancoins" class="size-6">
          <span class="text-2xl font-bold text-title">{{ gameInfos?.nyancoins }}</span>
        </div>
        <p class="text-text-main/60 text-sm">Nyancoins</p>
      </div>
      <div class="flex-center flex-col gap-2 p-6 rounded-2xl bg-surface">
        <span class="text-2xl font-bold text-title">
          {{ gameInfos.placable_pixels }}/{{ gameInfos.max_placable_pixels }}
        </span><p class="text-text-main/60 text-sm">Pixels disponibles</p>
      </div>
      <div class="flex-center flex-col gap-2 p-6 rounded-2xl bg-surface">
        <span class="text-2xl font-bold text-title">{{ gameInfos.unlocked_colors.length }}</span>
        <p class="text-text-main/60 text-sm text-center">Couleurs débloquées</p>
      </div>
    </div>
    <div class="w-full flex flex-wrap items-center justify-center gap-2" v-if="gameInfos">
      <div
        v-for="color in gameInfos.unlocked_colors"
        :key="color.hex_code"
        class="size-8 rounded-full border border-text-main/10"
        :style="{ backgroundColor: color.hex_code }"
        :title="color.name"
      />
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeMount, onMounted, ref } from 'vue';
import { storeToRefs }              from 'pinia';
import { useUserStore }             from '@storage';
import { getCookie }                from '@shared';
import Button                       from '@components/Button.vue';
import defaultCat                   from '@assets/default_cat.png';

const userStore = useUserStore();

const {
  userInfos,
  getLoggedStatus
} = storeToRefs(userStore);

const randomName    = "Stranger";
const username      = computed(() => userInfos.value?.username ?? randomName);
const profilePic    = computed(() => userInfos.value?.profile_image ?? defaultCat);
const email         = ref(userInfos.value?.email)
const newImageFile  = ref(null);
const newImage      = ref(null);
const gameInfos     = ref(null);

function onFileChange(e) {
 newImageFile.value = e.target.files[0];
 if (!newImageFile.value) return ;
 newImage.value = URL.createObjectURL(newImageFile.value);
}

const getGameInfos  = async () => {
  if (getLoggedStatus.value) {
    try {
      const response  = await fetch('/api/users/me/tplace/')
      if (!response.ok)
        throw new Error(`Couldn't get: ${response.status}`);
      return await response.json();
    }
    catch (error) {
      console.error(error.message);
      return null;
    }
  }
  return null;
};

const changeProfilePicture = async () => {
  const formData  = new FormData();
  formData.append('profile_image', newImageFile.value)
  try {
    const response = await fetch('/api/users/me/avatar/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    if (!response.ok)
      throw new Error(`Error: ${response.status}`);
    userStore.changeProfilePic(newImage.value);
    newImage.value = null;
  }
  catch (e) {
    console.error(e.message);
  }
}

onBeforeMount(async () => {
  gameInfos.value = await getGameInfos();
})
</script>

<style scoped>
</style>
