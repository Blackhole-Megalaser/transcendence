import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import svgLoader from 'vite-svg-loader'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    svgLoader(),
  ],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        skribbl: resolve(__dirname, 'skribbl.html'),
        tplace: resolve(__dirname, 'tplace.html'),
        privacy_policy: resolve(__dirname, 'privacypolicy.html'),
        term_of_service: resolve(__dirname, 'termService.html'),
		// chat: resolve(__dirname, 'chat.html'),
      },
    },
  },
});
