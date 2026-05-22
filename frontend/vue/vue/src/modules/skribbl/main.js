import { createApp } 		from 'vue';
import { setupPinia } 		from '@shared/pinia.js';
import App 					from './SkribbleApp.vue';
import { useThemeStore } 	from '@storage/theme.js';

import '@/style.css';

const pinia = setupPinia();
const app = createApp(App);
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);


app.mount('#app')