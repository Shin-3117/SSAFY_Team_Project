<template>
  <div>
    <div v-if="info">
      <h2>유저이름 : {{ info.username }}</h2>
      <p @click="followUser(info.id)">팔로우 하기</p>
      <p>이메일 : {{ info.email }}</p>
      <p>성별 : {{ info.gender===0 ? "남성" : "여성" }}</p>
      <p>생년월일 : {{ info.birthday }}</p>
      <div v-if="isLoading">Loading...</div>
      <div>
        {{ info }}
      </div>
      <br>
      <button v-if="userID===info.username"
      @click="()=>{deleteUserModal = !deleteUserModal}">회원탈퇴</button>
      <div v-if="deleteUserModal">
        <p>회원탈퇴 입력</p>
        <label for="DeleteID">
          아이디 : 
        </label><input type="text" id="DeleteID" v-model="deleteInfo.username">
        <label for="DeletePW">
          비밀번호 : 
        </label><input type="text" id="DeletePW" v-model="deleteInfo.password">
        <button @click="deleteUserR()">탈퇴하기</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { userInfo, deleteUser, followUser } from '@/api/userAPI'
import {useAuthStore} from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const username = ref(route.params.username)
const info = ref(null)
const isLoading = ref(true)
const userID = useAuthStore().userID

const deleteUserModal = ref(false)
const deleteInfo = ref({
  username: '',
  password: ''
})
const deleteUserR = async () => {
  try{
    await deleteUser(deleteInfo.value.username, deleteInfo.value.password)
    deleteInfo.value.username=''
    deleteInfo.value.password=''
    await router.push({path: "/article"})
  } catch(error) {
    console.error(error);
  }
}

onMounted(async () => {
  try {
    const response = await userInfo(username.value);
    info.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>

</style>