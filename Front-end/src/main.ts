import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// window.addEventListener('beforeunload', () => {
//   // 로컬 스토리지에서 'login' 데이터 삭제
//   localStorage.removeItem('login');
// });

app.mount('#app')
