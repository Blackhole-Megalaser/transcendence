import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia, fetchUserInfos }     from '@shared';
import Chat                             from '@components/Chat.vue'; 
import BasePage                         from '@components/BasePage.vue';
import SelectChat                       from '@components/SelectChat.vue';
import App                              from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

const userStore = useUserStore()
const userInfos = await userStore.initUserInfos();
if (!userInfos)
  window.location.href = '/login?next=/chat';
app.component('Chat', Chat);
app.component('SelectChat', SelectChat);
app.component('BasePage', BasePage);

app.mount('#app')
