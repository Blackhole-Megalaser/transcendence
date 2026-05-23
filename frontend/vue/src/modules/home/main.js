import { createApp } 		  from 'vue';
import HomeApp 				    from './HomeApp.vue';
import { useThemeStore } 	from '@storage/theme';

import { 
  setupPinia,
  Button,
  NavBar,
  SideBar,
  SideProfile
} from '@shared';

const app = createApp(HomeApp);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Button', Button);
app.component('NavBar', NavBar);
app.component('SideBar', SideBar);
app.component('SideProfile', SideProfile);

app.mount('#app')

