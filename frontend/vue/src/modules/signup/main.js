import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import { setupPinia }     from '@shared';
import BasePage           from '@components/BasePage.vue';
import Signup             from './localComponents/Signup.vue'; 
import App                from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Signup', Signup);
app.component('BasePage', BasePage);

app.mount('#app')
