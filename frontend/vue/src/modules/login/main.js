import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import { setupPinia }     from '@shared';
import BasePage           from '@components/BasePage.vue';
import Login              from './localComponents/Login.vue'; 
import App                from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Login', Login);
app.component('BasePage', BasePage);

app.mount('#app')
