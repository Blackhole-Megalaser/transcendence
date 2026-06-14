import { createApp, ref }                             from 'vue';
import { useThemeStore }                              from '@storage/theme';
import { setupPinia, fetchUserInfos, setupFontAwesome } from '@shared';
import BasePage                                       from '@components/BasePage.vue';
import TPlace                                         from './game/TPlace.vue'; 
import App                                            from './TplaceApp.vue';

const userInfos = await fetchUserInfos();
const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('TPlace', TPlace);
app.component('BasePage', BasePage);
app.provide('userInfos', ref(userInfos));
setupFontAwesome(app);

app.mount('#app')
