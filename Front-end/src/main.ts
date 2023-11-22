import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { setDefaultOptions } from 'date-fns';
import { ko } from 'date-fns/locale';

const app = createApp(App)

app.use(createPinia())
app.use(router)

// date-fns의 전역 로케일 설정
setDefaultOptions({ locale: ko });

app.mount('#app')
