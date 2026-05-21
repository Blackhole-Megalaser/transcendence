import { fileURLToPath } from 'url'
import path              from 'path';
import { dirname }       from 'path'
import { resolve }       from 'path'
import { defineConfig }  from 'vite'
import vue               from '@vitejs/plugin-vue'
import tailwindcss       from '@tailwindcss/vite'
import svgLoader         from 'vite-svg-loader'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

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
        main:             resolve(__dirname, 'index.html'),
        skribbl:          resolve(__dirname, 'skribbl.html'),
        tplace:           resolve(__dirname, 'tplace.html'),
        privacy_policy:   resolve(__dirname, 'privacypolicy.html'),
        term_of_service:  resolve(__dirname, 'termService.html'),
	      chat:             resolve(__dirname, 'chat.html'),
      },
    },
  },
  resolve: {
        alias: {
              '@assets':      path.resolve(__dirname, './src/assets'),
              '@components':  path.resolve(__dirname, './src/components'),
              '@modules':     path.resolve(__dirname, './src/modules'),
              '@chat':        path.resolve(__dirname, './src/modules/chat'),
              '@skribbl':     path.resolve(__dirname, './src/modules/skribbl'),
              '@tplace':      path.resolve(__dirname, './src/modules/tplace'),
              '@':            path.resolve(__dirname, './src'),
            },
    },
});
