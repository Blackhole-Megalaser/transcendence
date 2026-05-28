import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import { setupPinia }     from '@shared';
import BasePage           from '@components/BasePage.vue';
import App                from './App.vue';
import Update            from './update.vue'

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('BasePage', BasePage);
app.component('Profile', Profile);

app.mount('#app')
