import { defineStore } from 'pinia';

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    isLogin: false, // 초기 상태를 설정하세요
  }),
  getters: {
    // 필요한 경우 게터를 정의할 수 있습니다.
    // computed(()=>{})
  },
  actions: {
    // 상태를 업데이트하는 액션을 정의할 수 있습니다.
    toggleLogin() {
      this.isLogin = !this.isLogin;
    },
  },
});
