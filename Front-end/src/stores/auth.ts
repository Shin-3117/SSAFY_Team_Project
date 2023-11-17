import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import type { LogInInfo, SignUpInfo } from '@/interface/AuthType'
import config from '@/config'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = config.baseURL
  const token = ref(null)
  const userID = ref('')

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  
  const signUp = (payload: SignUpInfo) => {
    const { username, password1, password2, gender, birthday, money } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, 
        password1, 
        password2,
        gender,
        birthday,
        money
      }
    })
      .then((res) => {
        console.log(res)
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logIn = (payload: LogInInfo) => {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        console.log(res.data)
        token.value = res.data.key
        userID.value = username
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logOut = () => {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        token.value = null
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {signUp, logIn, token, isLogin, userID, logOut }
});
