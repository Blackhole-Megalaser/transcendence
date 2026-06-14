import { createPinia } 				    from "pinia";
import piniaPluginPersistedstate 	from 'pinia-plugin-persistedstate';
 let _pinia = null
export function setupPinia () {
  if (!_pinia) {
    _pinia = createPinia();
    _pinia.use(piniaPluginPersistedstate);
  }
  return (_pinia);
}
