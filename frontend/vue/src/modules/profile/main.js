import { createApp, ref }               from 'vue';
import { useThemeStore, useUserStore }  from '@storage';
import { setupPinia }                   from '@shared';
import BasePage                         from '@components/BasePage.vue';
import Profile                          from './Profile.vue'
import App                              from './App.vue';

const app = createApp(App);
const pinia = setupPinia();
app.use(pinia);

const userStore = useUserStore();
const userInfos = await userStore.initUserInfos();
// if (!userInfos)
//   window.location.href = '/login?next=/profile';

app.component('BasePage', BasePage);
app.component('Profile', Profile);

app.mount('#app');
