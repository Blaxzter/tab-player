/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// read BACKENDURL from .env file and set as axios base url
import axios from 'axios'
axios.defaults.baseURL = import.meta.env.VITE_BACKENDURL
console.log('BACKENDURL: ', import.meta.env.VITE_BACKENDURL)

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
