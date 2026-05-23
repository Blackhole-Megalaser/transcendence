import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import App                from './App.vue';

import {
  setupPinia,
  Button,
  NavBar,
  SideBar,
  SideProfile
} from '@shared';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Button', Button);
app.component('NavBar', NavBar);
app.component('SideBar', SideBar);
app.component('SideProfile', SideProfile);

app.mount('#app')
