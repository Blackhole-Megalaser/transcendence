import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import { setupPinia }     from '@shared';
import BasePage           from '@components/BasePage.vue';
import TPlace             from './game/TPlace.vue'; 
import App                from './TplaceApp.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('TPlace', TPlace);
app.component('BasePage', BasePage);

app.mount('#app')
