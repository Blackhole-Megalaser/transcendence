import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import Chat                             from '@components/Chat.vue'; 
import Skribbl                          from './App.vue';
import App                              from '@modules/skribbl/SkribbleApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('BasePage', BasePage);
app.component('Chat', Chat);
app.component('Skribbl', Skribbl);

app.mount('#app');