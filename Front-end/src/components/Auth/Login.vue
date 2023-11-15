<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
import { ref } from 'vue';

const authStore = useAuthStore()

const ID = ref('')
const IDerror = ref({
  'isError': false,
  'errorMsg': '아이디를 입력해 주세요!'
})
const PW = ref('')
const PWerror = ref({
  'isError': false,
  'errorMsg': '비밀번호를 입력해 주세요!'
})
const logIn = function () {
  const payload = {
    username: ID.value,
    password: PW.value
  }
  authStore.logIn(payload)
}
// const onSubmit = () => {
//   if(ID.value && PW.value){
//     authStore.toggleLogin()
//     IDerror.value.isError = false
//     PWerror.value.isError = false
//     props.loginState.open()
//   } else {
//     if(!ID.value){
//       IDerror.value.isError = true
//     } else {
//       IDerror.value.isError = false
//     }
//     if(!PW.value){
//       PWerror.value.isError = true
//     } else {
//       PWerror.value.isError = false
//     }
//   }
// }
</script>

<template>
<div class="background" v-on:click.self="loginState.open()">
  <section class="LoginFormBox">
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
      <input type="submit" value="로그인">
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
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.LoginFormBox{
  width: 340px;
  height: 200px;
  padding: 8px;
  background-color: aquamarine;
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
</style>