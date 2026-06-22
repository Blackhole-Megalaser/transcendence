import { createApp }                    from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import Signup                           from './localComponents/Signup.vue';
import App                              from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
const userInfos = await userStore.initUserInfos();
if (userInfos) {
  const queryParams     = new URLSearchParams(window.location.search);
  const room            = queryParams.get('room');
  let nextPage          = queryParams.get('next') ?? '/';
  let isSafeLink        = true;
  if (!nextPage.startsWith('/'))  nextPage    = '/' + nextPage;
  if (nextPage.length > 1)        isSafeLink  = !nextPage.startsWith('//');
  const dest            = new URL(isSafeLink ? nextPage : '/', window.location.origin);
  if (room)                       dest.searchParams.set('room', room);
  window.location.href  = dest.toString();
}

app.component('Signup', Signup);
app.component('BasePage', BasePage);

app.mount('#app');
