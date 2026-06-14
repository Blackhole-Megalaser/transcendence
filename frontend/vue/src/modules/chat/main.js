import { createApp, ref }           from 'vue';
import { useThemeStore }            from '@storage/theme';
import { setupPinia, getUserInfos } from '@shared';
import Chat                         from '@components/Chat.vue'; 
import BasePage                     from '@components/BasePage.vue';
import SelectChat                   from '@components/SelectChat.vue';
import App                          from './App.vue';

const userInfos = await getUserInfos();
if (!userInfos)
    window.location.href = '/login?next=/chat';
const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Chat', Chat);
app.component('SelectChat', SelectChat);
app.component('BasePage', BasePage);
app.provide('userInfos', ref(userInfos));

app.mount('#app')
