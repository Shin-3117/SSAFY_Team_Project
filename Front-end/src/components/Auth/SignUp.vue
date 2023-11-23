<template>
<div class="background">
  <div class="formBox bg-indigo-400 text-white dark:bg-slate-800
  animate-fade animate-once animate-duration-600
  rounded-lg">
    <div class="relative">
      <h2>Signup</h2>
      <button v-on:click="signupState.open()"
      class="absolute top-0 right-0 text-xl">✕</button>
    </div>

    <form @submit.prevent="signUp">
      <label for="ID">ID : 
        <span v-if="errors.username.state"
        class="text-red-500">
        {{ errors.username.message }}</span>
      </label>
      <input type="text" id="ID" v-model.trim="username">

      <label for="PW">비밀번호 : 
        <span v-if="errors.password1.state"
        class="text-red-500">
        {{ errors.password1.message }}</span>
      </label>
      <input type="password" id="PW" v-model.trim="password1">

      <label for="PW2">비밀번호 확인 : 
        <span v-if="errors.password2.state"
        class="text-red-500">
        {{ errors.password2.message }}</span>
      </label>
      <input type="password" id="PW2" v-model.trim="password2">

      <p>성별</p>
      <div class="flex">
        <label for="male">
          <input type="radio" name="gender" id="male" checked
          value="0" v-model="gender">남성
        </label>
        <label for="female">
          <input type="radio" name="gender" id="female"
          value="1" v-model="gender">여성
        </label>
      </div>

      <label for="birthday">생년월일
        <span v-if="errors.birthday.state"
        class="text-red-500">
        {{ errors.birthday.message }}</span>
      </label>
      <input type="date" id="birthday"
        min="1900-01-01" :max="today" v-model="birthday">

      <label for="money">보유자산</label>
      <input type="number" id="money" v-model="money">

      <br>
      <input type="submit" value="회원가입" class="Radio">
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
const gender = ref(0)
const birthday = ref(null)
const money = ref(0)

const todayTmp = new Date()
const year = todayTmp.getFullYear(); // 년도
const month = todayTmp.getMonth() + 1;  // 월
const date = todayTmp.getDate();  // 날짜

const today = ref(`${year}-${month}-${date}`)

const errors = ref({
  username: {
    state:false,
    message:'아이디를 입력해 주세요'
  },
  password1: {
    state:false,
    message:'비밀번호는 8글자 이상이여야 합니다.'
  },
  password2: {
    state:false,
    message:'입력한 비밀번호와 달라요'
  },
  birthday: {
    state:false,
    message:'생년월일을 입력해 주세요'
  }
})

const signUp = function () {
  if ( username.value!==null && 
      password1.value!==null && 
      password2.value!==null &&
      birthday.value!==null){

    const payload: SignUpInfo = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      gender: gender.value,
      birthday: birthday.value,
      money: money.value
    }
    store.signUp(payload)
    errors.value.birthday.state = false
    props.signupState.open()
  } else if(username.value===null ){
    errors.value.username.state = true
  } else if(password1.value===null || password1.value.length<8){
    errors.value.username.state = false
    errors.value.password1.state = true
  } else if(password2.value!==password1.value){
    errors.value.username.state = false
    errors.value.password1.state = false
    errors.value.password2.state = true
  } else if(birthday.value===null){
    errors.value.username.state = false
    errors.value.password1.state = false
    errors.value.password2.state = false
    errors.value.birthday.state = true
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
  z-index: 30;
  display: flex;
  justify-content: center;
  align-items: center;
  @apply text-black dark:text-white;
}
.formBox{
  width: 80%;
  max-width: 600px;
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

.Radio{
  @apply cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 
  text-white font-bold py-2 px-4 rounded-full mr-1;
}

input {
  color: black;
  @apply dark:text-white;
}
</style>