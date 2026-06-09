import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import { setupPinia }     from '@shared';
import BasePage           from '@components/BasePage.vue';
import Chat               from '@components/Chat.vue'; 
import SelectChat         from '@components/SelectChat.vue';
import App                from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Chat', Chat);
app.component('SelectChat', SelectChat);
app.component('BasePage', BasePage);

app.mount('#app')
