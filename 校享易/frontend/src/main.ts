// src/main.ts

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// 1. 完整引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 2. 将 Element Plus 注册到Vue应用中
app.use(ElementPlus)

app.mount('#app')