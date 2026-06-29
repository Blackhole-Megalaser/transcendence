import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia, setupFontAwesome }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import App                              from './LobbySkblApp.vue';
import GameRules                        from './gamerules/GameRules.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
userStore.initUserInfos();

app.component('BasePage', BasePage);
app.component('GameRules', GameRules);
setupFontAwesome(app);

app.mount('#app');
