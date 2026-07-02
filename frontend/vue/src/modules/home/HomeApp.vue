 <template>
  <BasePage :navBarVariant="navBarControl">
    <section class="text-text-main w-full flex-col flex gap-8 lg:gap-12 p-8 md:max-xl:pb-0 lg:pt-24!">
      
      <div class="justify-center gap-4 text-center">
        <h2>Welcome to FT_CAT!</h2>
        <p class="lg:max-w-2/3 mx-auto text-center opacity-90">
          FT_CAT, or ft_transcendence, is a 42 collaborative project started in late April 2026 by a group of five amazing 42 students.
          It features a multiplayer game (Skribbl.cat), a collaborative pixel art canvas (Tplace), and custom chat rooms !
        </p>
      </div>

      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 xl:gap-8 items-stretch w-full">
        
        <div class="cards flex flex-col h-full">
          <h3>Skribbl.cat</h3>
          <div class="w-full flex-1">
            <p class="text-justify">
              Skribbl.cat is a Pictionary-based game featuring one drawer and multiple guessers.<br>
              Guesser points are awarded based on how fast you find the right answer:
            </p>
            <ul class="w-full my-3 lg:pl-2 xl:pl-4">
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span><span class="font-bold text-title">200</span> points given to the 1st guesser</span>
              </li>
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span>Then points given to the next guessers decreases over time</span>
              </li>
            </ul>
            <p class="text-justify w-full">
              Meanwhile, drawer points depend on the other players' speed (and success of course):
            </p>
            <ul class="w-full my-3 lg:pl-2 xl:pl-4">
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span><span class="font-bold text-title">~70</span> points if a player guesses ultra fast</span>
              </li>
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span>Then points given to the drawer decreases over time and if nobody guesses right, no points are given</span>
              </li>
            </ul>
          </div>
          <a href="/lobbyskbl" class="mt-auto pt-6 w-full flex justify-center">
            <ButtonLogin>Play now !</ButtonLogin>
          </a>
        </div>

        <div class="cards flex flex-col h-full">
          <h3>Tplace</h3>
          <div class="w-full flex-1">
            <p class="text-justify">
              Love the concept of placing pixels with friends to create cool artwork as a community ? Transcendence's Place, alias Tplace, is the perfect match for you !
            </p>
            <ul class="w-full my-4 lg:pl-2 xl:pl-4">
              <li class="mb-2">
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span>Start with a pool of <span class="font-bold text-title">10</span> pixels to draw instantly.</span>
              </li>
              <li class="mb-2">
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span>Earn FT_CAT's official currency : <span class="font-bold text-title">NyanCoins</span> for each pixel you place !</span>
              </li>
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span>Spend your coins to upgrade your max <span class="font-bold text-title">pixel capacity</span> and reduce your cooldown to recover your pixels faster !</span>
              </li>
            </ul>
          </div>
          <a href="/tplace" class="mt-auto pt-6 w-full flex justify-center">
            <ButtonLogin>Draw now !</ButtonLogin>
          </a>
        </div>

        <div class="cards flex flex-col h-full">
          <h3>Chat rooms</h3>
          <div class="w-full flex-1">
            <p class="text-justify">
              Want to socialize, share game strategies, or just spam cat emojis? Jump into our live chat rooms and start gossiping with other students! We have three main rooms:
            </p>
            <ul class="w-full my-4 lg:pl-2 xl:pl-4">
              <li class="mb-3">
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span><span class="font-bold text-title">General</span>: The main hub to talk about everything and nothing.</span>
              </li>
              <li class="mb-3">
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span><span class="font-bold text-title">Cutie Cardboard</span>: A cozy, wholesome place for chill vibes and cute cat pics.</span>
              </li>
              <li>
                <span class="size-1.5 rounded-full bg-title shrink-0"></span>
                <span><span class="font-bold text-title">Naughty Cat's Hideout</span>: The secret corner for chaotic energy, banter, and late-night talks.</span>
              </li>
            </ul>
          </div>
          <a href="/chat" class="mt-auto pt-6 w-full flex justify-center">
            <ButtonLogin>Chat Now !</ButtonLogin>
          </a>
        </div>

      </section>
    </section>
  </BasePage>
</template>

<script setup>
import { 
  onMounted,
  onUnmounted, 
  provide,
  computed, 
  ref 
} from 'vue';

import { fetchFriends }  from '@shared';

const friendInfos         = ref({ status: '', friends: [], pending_friend_requests: []});
const scrollY             = ref(0);
const navBarControl       = computed(() => scrollY.value <= 0 ? 'home' : 'nav');
let   friendRequestTimer  = null;

provide('FRIENDREQUESTS', friendInfos);

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

function handleScroll() {
  scrollY.value = window.scrollY
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll);
  await refreshFriendRequest();
  friendRequestTimer  = setInterval(refreshFriendRequest, 5000);
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  clearInterval(friendRequestTimer);
})
</script>

<style scoped>
@import "@/style.css";

h2, h3 {
  @apply text-title font-bold;
}
h2 {
  @apply text-4xl lg:text-5xl
}
h3 {
  @apply text-3xl mb-4 text-center w-full
}
div {
  @apply flex items-center flex-col
}
li {
  @apply flex items-start gap-2.5 w-full text-justify
}
li > span:first-child {
  @apply mt-2
}
.cards {
  @apply bg-navbar/40 p-6 xl:p-8 rounded-4xl transition-all duration-300 border border-transparent hover:border-title/10 hover:-translate-y-2 hover:bg-navbar hover:shadow-xl
}
br {
  @apply mb-2
}
</style>
