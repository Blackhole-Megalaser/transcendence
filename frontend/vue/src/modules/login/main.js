import { createApp }                from 'vue';
import { useThemeStore }            from '@storage/theme';
import { setupPinia, getUserInfos } from '@shared';
import BasePage                     from '@components/BasePage.vue';
import Login                        from './localComponents/Login.vue'; 
import App                          from './App.vue';

const userInfos = await getUserInfos();
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
const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Login', Login);
app.component('BasePage', BasePage);

app.mount('#app')
