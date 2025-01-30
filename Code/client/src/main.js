import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import { authState } from './auth';

const app = createApp(App)

app.provide('authState', authState);

app.use(createPinia())
app.use(router)

app.mount('#app')
