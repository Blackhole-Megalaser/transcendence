import { createApp, ref }                from 'vue';
import { useThemeStore }            from '@storage/theme';
import { setupPinia, getUserInfos } from '@shared';
import BasePage                     from '@components/BasePage.vue';
import App                          from './App.vue';
import Update                       from './update.vue'

const userInfos = await getUserInfos();
const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('BasePage', BasePage);
app.component('Profile', Profile);
app.provide('userInfos', ref(userInfos));

app.mount('#app')
