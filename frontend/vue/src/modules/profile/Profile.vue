<template>
  <div>
    <img src="" alt="">
  </div>
	<div class="w-full h-full">
		<div class="grid grid-cols-2 lg:grid-cols-2 grid-rows-[3fr_1fr_1fr] lg:grid-rows-[1fr_0.30fr]
			gap-2 w-full h-full max-w-full max-h-full p-4
			bg-bg-main">
			<!-- __________ COLORS __________ -->
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
</template>
<script setup>
import { ref }      from 'vue';
import defaultcat   from '@assets/default_cat.png';

const ProfilePicture = ref()

let api_user    = ref(false);
let api_nyan    = ref(false);
let api_color   = ref(false);
let api_pixel   = ref(false);
let api_avatar  = ref(false);

let resp        = ref("nothing yet");

const getUser = async () => {
  api_user.value = !api_user.value

  try {
    const response  = await fetch('/api/users/me/')
    if (!response.ok)
      throw new Error(`Couldn't get: ${response.status}`);
    resp.value = await response.json();
  }
  catch (error) {
    console.error(error.message);
  }
};

const getNyan = async () => {
  api_nyan.value = !api_nyan.value

  try {
    const response  = await fetch('/api/users/me/nyancoins')
    if (!response.ok)
      throw new Error(`Couldn't get: ${response.status}`);
    resp.value = await response.json();
  }
  catch (error) {
    console.error(error.message);
  }
};

const getColor = async () => {
  api_color.value = !api_color.value

  try {
    const response  = await fetch('/api/users/me/colors')
    if (!response.ok)
      throw new Error(`Couldn't get: ${response.status}`);
    resp.value = await response.json();
  }
  catch (error) {
    console.error(error.message);
  }
};

const getPixel = async () => {
  api_pixel.value = !api_pixel.value

  try {
    const response  = await fetch('/api/users/me/pixels')
    if (!response.ok)
      throw new Error(`Couldn't get: ${response.status}`);
    resp.value = await response.json();
  }
  catch (error) {
    console.error(error.message);
  }
};

const getAvatar = async () => {
  api_avatar.value = !api_avatar.value

  try {
    const response  = await fetch('/api/users/me/')
    if (!response.ok) {
      throw new Error(`Couldn't get: ${response.status}`);
    }
    resp.value = await response.json();
  }
  catch (error) {
    console.error(error.message);
  }
};

</script>

<style scoped>
</style>
