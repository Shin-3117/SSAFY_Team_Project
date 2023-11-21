<template>
  <div>
    <!-- <p>store 사용</p> -->
    <button v-if="!authStore.isLogin" 
      v-on:click="openLogin.open()"
      class="btn btn-blue">로그인</button>
    <Login v-if="openLogin.state" :login-state="openLogin"/>

    <button v-if="!authStore.isLogin"
      v-on:click="openSignUp.open()"
      class="btn btn-blue">회원가입</button>
    <SignUp v-if="openSignUp.state" :signup-state="openSignUp"/>

    <button v-if="authStore.isLogin" class="btn btn-blue">
      <RouterLink :to="`/userInfo/${authStore.userID}`" 
        >회원정보</RouterLink>
    </button>
    
    <button v-if="authStore.isLogin" 
      v-on:click="authStore.logOut"
      class="btn btn-blue">로그아웃</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import Login from './Login.vue';
import SignUp from './SignUp.vue';

const authStore = useAuthStore()
const openLogin = ref({
  state:false,
  open(){
    this.state = !this.state
  }
})
const openSignUp = ref({
  state:false,
  open(){
    this.state = !this.state
  }
})
</script>

<style scoped lang="scss">
.btn {
  @apply font-bold py-2 px-4 rounded-full;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>