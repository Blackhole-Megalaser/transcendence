import { defineStore } from "pinia";

const THEMES = ["light", "dark"];

export const useThemeStore = defineStore("theme", {
  state: () => ({
    current: "light"
  }),
  actions: {
    setTheme(theme) {
      if (!THEMES.includes(theme)) return;
      this.current = theme;
      document.documentElement.setAttribute("data-theme", theme);
    },
    cycle() {
      const next = THEMES[(THEMES.indexOf(this.current) + 1) % THEMES.length];
      this.setTheme(next);
    },
    getThemeIndex() {
      return THEMES.indexOf(this.current) % THEMES.length;
    }
  },
  persist: {
    key: "app-theme"
  }
});