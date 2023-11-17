<template>
  <div>
    <div v-if="info">
      <h2>유저이름 : {{ info.username }}</h2>
      <p>이메일 : {{ info.email }}</p>
      <p>성별 : {{ info.gender===0 ? "남성" : "여성" }}</p>
      <p>생년월일 : {{ info.birthday }}</p>
      <div v-if="isLoading">Loading...</div>
      <div>
        {{ info }}
      </div>
    </div>
    <button @click="deleteUserR">회원탈퇴</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { userInfo, deleteUser } from '@/api/userAPI'

const route = useRoute()
const router = useRouter()
const username = ref(route.params.username)
const info = ref(null)
const isLoading = ref(true)

const deleteUserR = async () => {
  try{
    await deleteUser()
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