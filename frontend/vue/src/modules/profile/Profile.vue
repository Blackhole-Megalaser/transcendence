<!-- <template>
  <div>
    <img src="" alt="">
  </div>
	<div class="w-full h-full">
		<div class="grid grid-cols-2 lg:grid-cols-2 grid-rows-[3fr_1fr_1fr] lg:grid-rows-[1fr_0.30fr]
			gap-2 w-full h-full max-w-full max-h-full p-4
			bg-bg-main">
			<div
				:style="[cursorStyle, {backgroundColor: penColor}]" 
				class="order-1 row-start-1 lg:row-start-1  col-start-1 lg:col-start-1
					grid grid-flow-col grid-rows-1 justify-center
					h-full w-full max-w-full max-h-full min-h-0 
					bg-sidebar border-5 border-solid rounded-4xl overflow-hidden border-button-1-normal">
				<button :style="[cursorStyle, {backgroundColor: penColor}]"
					class="bg-sidebar w-full h-full overflow-hidden">
					<svg class="stroke-[0.5]  w-full h-full"
							xlms="http://www.w3.org/2000/svg"
							viewBox="0 0 32 32"
							stroke-width="2" stroke-miterlimit="10">
						<ellipse class="stroke-[0.7] stroke-[#917F97] fill-pink-50" cx="16" cy="18" rx="13" ry="15"/>
						<ellipse 
              :class="api_user ? 'stroke-blue-500 fill-sky-100' 
                : 'stroke-blue-600 fill-blue-500 hover:stroke-blue-500 hover:fill-blue-400'" 
              @click="getUser()" cx="12.5" cy="9.5" rx="2.5" ry="3.5" 
              title="user :3"/>
						<ellipse 
              :class="api_nyan ? 'stroke-red-500 fill-sky-100' 
                : 'stroke-red-600 fill-red-500 hover:stroke-red-500 hover:fill-red-400'" 
              @click="getNyan()" cx="19.5" cy="9.5" rx="2.5" ry="3.5" 
              title="nyan :3" />
						<ellipse 
              :class="api_color ? 'stroke-green-500 fill-sky-100' 
                  : 'stroke-green-600 fill-green-500 hover:stroke-green-500 hover:fill-green-400'" 
              @click="getColor()" cx="7.5" cy="16.5" rx="2.5" ry="3.5" 
              title="color :3" alt="COULEUR"/>
						<ellipse 
              :class="api_pixel ? 'stroke-yellow-500 fill-sky-100' 
                  : 'stroke-yellow-600 fill-yellow-500 hover:stroke-yellow-500 hover:fill-yellow-400'" 
              @click="getPixel()" cx="24.5" cy="16.5" rx="2.5" ry="3.5" 
              title="pixel :3" />
						<path 
              :class="api_avatar ? 'stroke-gray-800 fill-sky-100' 
                  : 'stroke-gray-800 fill-black hover:stroke-gray-800 hover:fill-gray-900'" 
              @click="getAvatar()" 
              title="avatar :3" d="M19,20c-0.966-0.966-1-3-3-3s-2,2-3,3
							s-4,1.069-4,3.5c0,1.381,1.119,2.5,2.5,2.5c1.157,0,3.684-1,4.5-1s3.343,1,4.5,1c1.381,0,2.5-1.119,2.5-2.5
							C23,21.207,19.966,20.966,19,20z"/>
						<rect class="stroke-[#917F97] fill-pink-50" x="5.5" y="27" width="21" height="32"></rect>
						<rect class="fill-pink-50" x="5.75" y="26.5" width="20.5" height="32"></rect>
					</svg>
				</button>
			</div>
      <div
          class="order-2 row-start-1 lg:row-start-1  col-start-2 lg:col-start-2
					grid grid-flow-col grid-rows-1 justify-center
					h-full w-full max-w-full max-h-full min-h-0 
					bg-sidebar border-5 border-solid rounded-4xl overflow-hidden border-button-1-normal">
          <div>
					  <p>DATA LOL</p>
					  <p>user:{{ api_user }}</p>
            <p>nyan:{{ api_nyan }}</p>
            <p>color:{{ api_color }}</p>
            <p>pixel:{{ api_pixel }}</p>
            <p>avatar:{{ api_avatar }}</p>
            <p>response: {{ resp }}</p>
				  </div>
        </div>
		</div>
	</div>
</template> -->

<template>
  <section class="w-full flex-center flex-col gap-8 lg:gap-12 p-8 md:max-xl:pb-0 lg:pt-24!">
    <div class="flex items-end">
      <div 
        class="size-24 rounded-full bg-cover bg-center cursor-pointer"
        :style="{ backgroundImage: `url(${profilePic})` }"
        @click="$refs.fileInput.click()"
      />
      <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange">
      <div v-if="newImage">
        <p class="text-text-main/60">{{ newImageFile.name }}</p>
        <Button @click="changeProfilePicture()">Submit</Button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { storeToRefs }              from 'pinia';
import { useUserStore }             from '@storage';
import { getCookie }                from '@shared';
import Button                       from '@components/Button.vue';
import defaultCat                   from '@assets/default_cat.png';

const userStore = useUserStore();
const {
  getProfilePic,
  getLoggedStatus
} = storeToRefs(userStore);
const profilePic  = computed(() => getProfilePic.value ?? defaultCat);
const newImageFile= ref(null);
const newImage    = ref(null);
const gameInfos   = ref(null);
const response    = ref(null);

function onFileChange(e) {
 newImageFile.value = e.target.files[0];
 if (!newImageFile.value) return ;
 newImage.value = URL.createObjectURL(newImageFile.value);
 console.log(newImageFile.value);
}

const getGameInfos  = async () => {
  if (getLoggedStatus.value) {
    try {
      const ret  = await fetch('/api/users/me/tplace/')
      if (!ret.ok)
        throw new Error(`Couldn't get: ${ret.status}`);
      response.value = await ret.json();
    }
    catch (error) {
      console.error(error.message);
    }
  }
};

const changeProfilePicture = async () => {
  const formData  = new FormData();
  formData.append('profile_image', newImageFile.value)
  try {
    const ret = await fetch('api/users/me/avatar/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    if (!ret.ok)
      throw new Error(`Error: ${response.status}`);
    userStore.changeProfilePic(newImage.value);
    newImage.value = null;
  }
  catch (e) {
    console.error(e.message);
  }
}

onMounted(async () => {
  gameInfos.value = await getGameInfos();
})
</script>

<style scoped>
</style>
