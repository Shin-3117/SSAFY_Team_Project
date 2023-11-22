<template>
  <div>
    <!-- <p>store 사용</p> -->
    <button v-if="!authStore.isLogin" 
      v-on:click="openLogin.open()"
      class="Radio">로그인</button>
    <Login v-if="openLogin.state" :login-state="openLogin"/>

    <button v-if="!authStore.isLogin"
      v-on:click="openSignUp.open()"
      class="Radio">회원가입</button>
    <SignUp v-if="openSignUp.state" :signup-state="openSignUp"/>

    <button v-if="authStore.isLogin" class="Radio">
      <RouterLink :to="`/userInfo/${authStore.userID}`" 
        >회원정보</RouterLink>
    </button>
    
    <button v-if="authStore.isLogin" 
      v-on:click="authStore.logOut"
      class="Radio">로그아웃</button>
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
.Radio{
  @apply cursor-pointer bg-indigo-400 hover:bg-gradient-to-br from-purple-600 to-blue-500 
  text-white font-bold py-2 px-4 rounded-full mr-1;
}
</style>