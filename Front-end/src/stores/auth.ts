 import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import type { LogInInfo, SignUpInfo } from '@/interface/AuthType'
import config from '@/config'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = config.baseURL
  const token = ref(null)
  const userID = ref('')

  if (token.value===null){
    const LoginHistory = localStorage.getItem('login')
    if (typeof(LoginHistory)==='string') {
      const objData = JSON.parse(LoginHistory)
      userID.value = objData.username
      token.value = objData.token
    }
    // console.log(LoginHistory)
  }


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
        const localValue = {
          username: username,
          token: res.data.key
        }
        localStorage.setItem('login', JSON.stringify(localValue))
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
        localStorage.removeItem('login')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {signUp, logIn, token, isLogin, userID, logOut }
});
