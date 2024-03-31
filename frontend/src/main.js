import { createApp } from 'vue'
import vuetify from "@/plugins/vuetify.js";
import App from './views/YTDownloader.vue'
import "@/assets/base.css"

createApp(App).use(vuetify).mount('#app')
