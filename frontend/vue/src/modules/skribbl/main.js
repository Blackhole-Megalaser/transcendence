import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia, setupFontAwesome }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import Skribbl                          from './game/Skribbl.vue';
import Chat                             from '@components/Chat.vue'; 
import App                              from './SkribbleApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('BasePage', BasePage);
app.component('Chat', Chat);
app.component('Skribbl', Skribbl);
setupFontAwesome(app);

app.mount('#app');
