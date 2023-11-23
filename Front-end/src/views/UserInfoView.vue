<template>
  <div class="animate-fade animate-once animate-duration-[1500ms] mx-auto w-2/4">
    <div v-if="isLoading">Loading...</div>
    <div v-if="info" class="border-4 border-indigo-300 my-4 rounded-xl p-4 bg-indigo-50">
      <p v-if="userID !== info.username" @click="followUser(info.id)">
      <div class="Radio w-32 text-center">팔로우 하기</div>
      </p>
      <h2 class="mt-4 text-xl font-extrabold">유저이름 : {{ info.username }}</h2>
      <p class="mt-4 text-lg font-semibold">이메일 : {{ info.email }}</p>
      <p class="mt-4 text-lg font-semibold">성별 : {{ info.gender === 0 ? "남성" : "여성" }}</p>
      <p class="mt-4 text-lg font-semibold">생년월일 : {{ info.birthday }}</p>
      <p class="my-4 text-lg font-semibold">보유금액 : {{ info.money }}</p>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">작성한 게시글</p>
        <ul>
          <li v-for="written_article in info.written_articles" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <RouterLink :to="`/article/${written_article.id}`">
              <p>{{ written_article.title }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">작성한 댓글</p>
        <ul>
          <li v-for="written_comment in info.written_comments" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <RouterLink :to="`/article/${written_comment.article}`">
              <p>{{ written_comment.content }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">좋아요한 게시글</p>
        <ul>
          <li v-for="liked_article in info.liked_articles" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <RouterLink :to="`/article/${liked_article.id}`">
              <p>{{ liked_article.title }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">팔로잉</p>
        <ul>
          <li v-for="following in info.followings_list" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <RouterLink :to="`/userInfo/${following.username}`">
              <p>{{ following.username }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">팔로워</p>
        <ul>
          <li v-for="follower in info.followers_list" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <RouterLink :to="`/userInfo/${follower.username}`">
              <p>{{ follower.username }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">즐겨찾기한 예금</p>
        <ul>
          <li v-for="deposit in info.deposit_subscriptions" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <p>{{ deposit.deposit_product_detail.fin_prdt_nm }} {{ deposit.deposit_option_detail.save_trm }}개월</p>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <div>
        <p class="mt-4 text-xl font-semibold">즐겨찾기한 적금</p>
        <ul>
          <li v-for="deposit in info.saving_subscriptions" class="cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white rounded-lg text-center w-fit px-4 my-2">
            <p>{{ deposit.saving_product_detail.fin_prdt_nm }} {{ deposit.saving_option_detail.save_trm }}개월</p>
          </li>
        </ul>
      </div>
      <hr class="border-2 border-indigo-300">
      <!-- <div>
        {{ info }}
      </div> -->
      <br>
      <button v-if="userID === info.username" @click="() => { deleteUserModal = !deleteUserModal }" class="cursor-pointer bg-red-500 hover:bg-red-700 text-white rounded-lg text-center w-fit p-2 my-2">회원탈퇴</button>
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
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { userInfo, deleteUser, followUser } from '@/api/userAPI'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const username = ref('')
const info = ref(null)
const isLoading = ref(true)
const userID = useAuthStore().userID

const deleteUserModal = ref(false)
const deleteInfo = ref({
  username: '',
  password: ''
})
const deleteUserR = async () => {
  try {
    await deleteUser(deleteInfo.value.username, deleteInfo.value.password)
    deleteInfo.value.username = ''
    deleteInfo.value.password = ''
    await router.push({ path: "/article" })
  } catch (error) {
    console.error(error);
  }
}



// 라우트 파라미터 변경 감시
watch(() => route.params.username, async (newUsername) => {
  username.value = newUsername;
  isLoading.value = true;
  try {
    const response = await userInfo(newUsername);
    info.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
}, { immediate: true });

onMounted(async () => {
  // 초기 데이터 로드
  username.value = route.params.username;
  try {
    const response = await userInfo(username.value);
    info.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.Radio {
  @apply cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 text-white font-bold py-2 px-4 rounded-full mr-1;
}
</style>