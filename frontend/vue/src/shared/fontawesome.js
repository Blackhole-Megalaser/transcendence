import { library }         from '@fortawesome/fontawesome-svg-core';
import { fab }             from '@fortawesome/free-brands-svg-icons';
import { far }             from '@fortawesome/free-regular-svg-icons';
import { fas }             from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

function mapIconsByName(pack) {
  return Object.fromEntries(
    Object.values(pack)
      .filter((icon) => icon && typeof icon === 'object' && icon.iconName)
      .map((icon) => [icon.iconName, icon])
  );
}

export const byPrefixAndName = {
  fas: mapIconsByName(fas),
  far: mapIconsByName(far),
  fab: mapIconsByName(fab),
};

library.add(fas, far, fab);

export function setupFontAwesome(app) {
  app.component('FontAwesomeIcon', FontAwesomeIcon);
  app.component('font-awesome-icon', FontAwesomeIcon);
  app.config.globalProperties.byPrefixAndName = byPrefixAndName;
}

// FontAwesome icon usage
// In a main.js file:
// 	import { setupFontAwesome } from '@shared';
// then call setupFontAwesome(app)
// In a Vue component:
// 	<font-awesome-icon :icon="['fas', 'house']" />.
// 	<FontAwesomeIcon :icon="byPrefixAndName.fas['house']" />.
