<template>
<div class="background" v-on:click.self="signupState.open()">
  <div class="formBox bg-slate-200 dark:bg-slate-800">
    <h2>Signup</h2>
    <form @submit.prevent="signUp">
      <label for="ID">ID : </label>
      <input type="text" id="ID" v-model.trim="username">

      <label for="PW">비밀번호 : </label>
      <input type="password" id="PW" v-model.trim="password1">

      <label for="PW2">비밀번호 확인 : </label>
      <input type="password" id="PW2" v-model.trim="password2">
      <br>
      <input type="submit" value="회원가입" class="btn btn-blue">
    </form>
  </div>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { SignUpInfo } from '@/interface/AuthType.js'
const store = useAuthStore()
const props = defineProps(['signupState'])

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  if ( username.value!==null && 
      password1.value!==null && 
      password2.value!==null){

    const payload: SignUpInfo = {
      username: username.value,
      password1: password1.value,
      password2: password2.value
    }
    store.signUp(payload)
  } else {
    window.alert('양식오류')
  }
}
</script>

<style scoped lang="scss">
.background{
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0; left: 0;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.formBox{
  width: 80%;
  height: 80%;
  padding: 8px;
  h2{
    text-align: center;
    font-size: larger;
    padding: 8px;
  }
}
form{
  display: flex;
  flex-direction: column;
}

.btn {
  @apply font-bold py-2 px-4 rounded-full;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>@/interface/AuthType