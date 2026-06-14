import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia, fetchUserInfos }     from '@shared';
import App                              from './HomeApp.vue';
import BasePage                         from '@components/BasePage.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

const userStore = useUserStore()
const userInfos = await userStore.initUserInfos();

app.component('BasePage', BasePage);

app.mount('#app')
