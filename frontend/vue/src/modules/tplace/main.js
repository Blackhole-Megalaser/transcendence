import { createApp }      from 'vue';
import { useThemeStore }  from '@storage/theme';
import App                from './TplaceApp.vue';
import TPlace 		        from './game/TPlace.vue';

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

app.component('TPlace', TPlace);
app.component('Button', Button);
app.component('NavBar', NavBar);
app.component('SideBar', SideBar);
app.component('SideProfile', SideProfile);

app.mount('#app')
