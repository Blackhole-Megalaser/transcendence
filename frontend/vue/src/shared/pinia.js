import { createPinia } 				from "pinia";
import piniaPluginPersistedstate 	from 'pinia-plugin-persistedstate';

export function setupPinia () {
  const pinia = createPinia();
  pinia.use(piniaPluginPersistedstate);
  return (pinia);
}