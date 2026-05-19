import { createApp } from 'vue';
import { setupPinia } from '../../shared/pinia';
import ChatApp from './ChatApp.vue';
import { useThemeStore } from '../../storage/theme';

const pinia = setupPinia();
const app = createApp(ChatApp);
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);


app.mount('#app')
