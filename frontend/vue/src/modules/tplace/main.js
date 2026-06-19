import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia, setupFontAwesome } from '@shared';
import BasePage                         from '@components/BasePage.vue';
import TPlace                           from './game/TPlace.vue'; 
import App                              from './TplaceApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('BasePage', BasePage);
app.component('TPlace', TPlace);
setupFontAwesome(app);

app.mount('#app');
