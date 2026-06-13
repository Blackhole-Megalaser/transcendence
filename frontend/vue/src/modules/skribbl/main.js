import { createApp, ref }                from 'vue';
import { useThemeStore }            from '@storage/theme';
import { setupPinia, getUserInfos } from '@shared';
import BasePage                     from '@components/BasePage.vue';
import Skribbl                      from './game/Skribbl.vue';
import App                          from './SkribbleApp.vue';

const userInfos = await getUserInfos();
const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Skribbl', Skribbl);
app.component('BasePage', BasePage);
app.provide('userInfos', ref(userInfos));

app.mount('#app')
