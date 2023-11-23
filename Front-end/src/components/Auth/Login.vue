<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
import { ref } from 'vue';

const authStore = useAuthStore()
const props = defineProps(['loginState'])

const ID = ref(null)
const IDerror = ref({
  'isError': false,
  'errorMsg': '아이디를 입력해 주세요!'
})
const PW = ref(null)
const PWerror = ref({
  'isError': false,
  'errorMsg': '비밀번호를 입력해 주세요!'
})

const logIn = function () {
  if(ID.value && PW.value){
    const payload = {
      username: ID.value,
      password: PW.value
    }
    authStore.logIn(payload)

    IDerror.value.isError = false
    PWerror.value.isError = false
    props.loginState.open()
  } else {
    if(!ID.value){
      IDerror.value.isError = true
    } else {
      IDerror.value.isError = false
    }

    if(!PW.value){
      PWerror.value.isError = true
    } else {
      PWerror.value.isError = false
    }
  }
}
</script>

<template>
<div class="background" v-on:click.self="loginState.open()">
  <section class="LoginFormBox bg-slate-700 dark:bg-slate-800">
    <h2>Login</h2>
    <form v-on:submit.prevent="logIn">
      <label for="ID">아이디 입력
        <span class="errorMsg">{{ IDerror.isError ? IDerror.errorMsg : '' }}</span>
      </label>
      <input type="text" id="ID" v-model="ID">
      <br>
      <label for="PW">비밀번호 입력
        <span class="errorMsg">{{ PWerror.isError ? PWerror.errorMsg : '' }}</span>
      </label>
      <input type="password" id="PW" v-model="PW">
      <br>
      <input type="submit" value="로그인" class="btn btn-blue">
    </form>
  </section>
</div>
</template>

<style scoped lang="scss">
.background{
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0; left: 0;
  z-index: 20;
  display: flex;
  justify-content: center;
  align-items: center;
  @apply text-black dark:text-white;
}
.LoginFormBox{
  width: 80%;
  max-width: 400px;
  padding: 20px;
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
.errorMsg{
  color: rgb(192, 2, 2);
}
.btn {
  @apply font-bold py-2 px-4;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>