import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import Skribbl                          from './game/Skribbl.vue';
import App                              from './SkribbleApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('Skribbl', Skribbl);
app.component('BasePage', BasePage);

app.mount('#app');
