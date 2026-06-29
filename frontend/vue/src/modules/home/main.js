import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import ButtonLogIn                      from '@components/ButtonLogIn.vue';
import App                              from './HomeApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('BasePage', BasePage);
app.component('ButtonLogin', ButtonLogIn)

app.mount('#app');
