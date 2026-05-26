import { library }         from '@fortawesome/fontawesome-svg-core';
import { fab }             from '@fortawesome/free-brands-svg-icons';
import { far }             from '@fortawesome/free-regular-svg-icons';
import { fas }             from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(fas, far, fab);

export function setupFontAwesome(app) {
  app.component('font-awesome-icon', FontAwesomeIcon);
}

// FontAwesome icon usage
// In a main.js file:
// 	import { setupFontAwesome } from '@shared';
// then call setupFontAwesome(app)
// In a Vue component:
// 	<font-awesome-icon :icon="['fas', 'house']" />.
