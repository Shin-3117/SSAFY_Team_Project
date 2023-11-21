<template>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="info">
      <p @click="followUser(info.id)">팔로우 하기</p>
      <h2>유저이름 : {{ info.username }}</h2>
      <p>이메일 : {{ info.email }}</p>
      <p>성별 : {{ info.gender===0 ? "남성" : "여성" }}</p>
      <p>생년월일 : {{ info.birthday }}</p>
      <p>보유금액 : {{ info.money }}</p>
      <hr>
      <div>
        <p>작성한 게시글</p>
        <ul>
          <li v-for="written_article in info.written_articles">
            <RouterLink :to="`/article/${written_article.id}`">
              <p>{{ written_article.title }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>작성한 댓글</p>
        <ul>
          <li v-for="written_comment in info.written_comments">
            <RouterLink :to="`/article/${written_comment.article}`">
              <p>{{ written_comment.content }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>좋아요한 게시글</p>
        <ul>
          <li v-for="liked_article in info.liked_articles">
            <RouterLink :to="`/article/${liked_article.id}`">
              <p>{{ liked_article.title }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>팔로잉</p>
        <ul>
          <li v-for="following in info.followings_list">
            <p>{{ following }}</p>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>팔로워</p>
        <ul>
          <li v-for="follower in info.followers_list">
            <p>{{ follower.username }}</p>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>즐겨찾기한 예금</p>
        <ul>
          <li v-for="deposit in info.deposit_subscriptions">
            <p>{{ deposit.deposit_product_detail.fin_prdt_nm }}</p>
          </li>
        </ul>
      </div>
      <hr>
      <div>
        <p>즐겨찾기한 적금</p>
        <ul>
          <li v-for="deposit in info.saving_subscriptions">
            <p>{{ deposit.saving_product_detail.fin_prdt_nm }}</p>
          </li>
        </ul>
      </div>
      <hr>
      <!-- <div>
        {{ info }}
      </div> -->
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