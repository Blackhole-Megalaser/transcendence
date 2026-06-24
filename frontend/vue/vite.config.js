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
        main:           resolve(__dirname, 'index.html'),
        skribbl:        resolve(__dirname, 'skribbl.html'),
        tplace:         resolve(__dirname, 'tplace.html'),
        privacy:        resolve(__dirname, 'privacy.html'),
        terms:          resolve(__dirname, 'terms.html'),
        chat:           resolve(__dirname, 'chat.html'),
        login:          resolve(__dirname, 'login.html'),
        signup:         resolve(__dirname, 'signup.html'),
        profile:        resolve(__dirname, 'profile.html'),
        profile_update: resolve(__dirname, 'profileUpdate.html'),
        error_404:      resolve(__dirname, 'error_404.html'),
        error_50x:      resolve(__dirname, 'error_50x.html'),
      },
    },
  },
  resolve: {
    alias: {
      '@assets':      path.resolve(__dirname, './src/assets'),
      '@components':  path.resolve(__dirname, './src/components'),
      '@modules':     path.resolve(__dirname, './src/modules'),
      '@skribbl':     path.resolve(__dirname, './src/modules/skribbl'),
      '@tplace':      path.resolve(__dirname, './src/modules/tplace'),
      '@shared':      path.resolve(__dirname, './src/shared/'),
      '@storage':     path.resolve(__dirname, './src/storage'),
      '@':            path.resolve(__dirname, './src'),
    },
  },
});
