<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="signUp">
      <input type="text" v-model.trim="username">
      <input type="password" v-model.trim="password">
      <input type="password" v-model.trim="password2">
      <input type="submit">
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type UserInfo from '@/interface/Auth';
const store = useAuthStore()
const username = ref(null)
const password = ref(null)
const password2 = ref(null)

const signUp = function () {
  if ( username.value!==null && 
      password.value!==null && 
      password2.value!==null){

    const payload: UserInfo = {
      username: username.value,
      password: password.value,
      password2: password2.value
    }
    store.signUp(payload)
  } else {
    window.alert('양식오류')
  }
}
</script>

<style scoped>

</style>