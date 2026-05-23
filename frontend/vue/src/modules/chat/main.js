import { createApp } 		  from 'vue';
import { useThemeStore } 	from '@storage/theme';
import Chat               from '@components/Chat.vue'; 
import ChatApp 				    from './ChatApp.vue';

import { 
  setupPinia,
  Button,
  NavBar,
  SideBar,
  SideProfile
} from '@shared';

const app = createApp(ChatApp);
const pinia = setupPinia();
app.use(pinia);

const savedTheme = useThemeStore();
document.documentElement.setAttribute("data-theme", savedTheme.current);

app.component('Chat', Chat);
app.component('Button', Button);
app.component('NavBar', NavBar);
app.component('SideBar', SideBar);
app.component('SideProfile', SideProfile);

app.mount('#app')
