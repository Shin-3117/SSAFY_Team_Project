<template>
  <main class=" p-4 flex justify-center">
    <div class="p-4" v-if="Article">
      <RouterLink to="/article" class="text-blue-500 hover:underline mb-2">게시판으로</RouterLink>
      <h2 class="text-2xl font-bold mb-2">{{ Article.title }}</h2>
      <div class="flex justify-between">
        <RouterLink :to="`/userInfo/${Article.user.username}`" class="text-blue-500 hover:underline mb-2">
          <span>작성자: {{ Article.user.username }}</span>
        </RouterLink>
        <!-- <span>{{ Article.updated_at }}</span> -->
        <div v-if="isWriter" class="">
          <RouterLink :to="`/article/${Article.id}/put`" class="">수정하기</RouterLink> | 
          <button @click="deleteArticleR(Article.id)" class="">삭제</button>
        </div>
      </div>

      

      <div v-html="Article.content" class="mt-4"></div>
      <button @click="likeArticleR(Article.id)" class="btn btn-blue my-4">
        <img v-if="!isLike" src="../../assets/img/like-null.png" alt="LikeButton" class="w-6 h-6">
        <img v-if="isLike" src="../../assets/img/like-fill.png" alt="LikeButton" class="w-6 h-6">
      </button>
      
      <hr class="my-4">

      <form v-on:submit.prevent="postCommentR(Article.id, commentContent)" class="flex">
        <input type="text" id="content" v-model="commentContent" class="input">
        <input type="submit" value="댓글작성" class="btn btn-blue w-24">
      </form>

      <div v-if="Article.comments" class="space-y-4 ">
        <p class="font-bold">댓글 {{ Article.comments.length }}</p>
        <hr class="my-2">
        <ul v-for="comment in Article.comments" :key="comment.id" class="space-y-2">
          <li class="items-start">
            <p class="font-bold">{{ comment.user.username }}</p>
            <div class="flex-grow">
              <p>{{ comment.content }}</p>
              <div class="flex space-x-2" v-if="authStore.userID===comment.user.username ? true : false">
                <button @click="()=>{putId=comment.id; putContent=comment.content}" class="btn btn-gray">수정</button>
                <button @click="deleteComment(Article.id, comment.id)" class="btn btn-red">삭제</button>
              </div>

              <form v-on:submit.prevent="putComment(Article.id, comment.id, putContent,comment.user.username)" 
              v-if="putId===comment.id" class="flex">
                <input type="text" v-model="putContent" class="input">
                <input type="submit" value="수정하기" class="btn btn-blue w-24">
              </form>

              <details v-if="comment.replies" class="">
                <summary class="font-bold cursor-pointer">대댓글 {{ comment.replies.length }} | </summary>
                <form v-on:submit.prevent="postCommentR(Article.id, replieContent, comment.id)" class="flex">
                  <input type="text" v-model="replieContent" class="input">
                  <input type="submit" value="대댓글작성" class="btn btn-blue w-28">
                </form>


                <ul v-for="replie in comment.replies" :key="replie.id" class="ml-4 space-y-2">
                  <li >
                    <div class="flex items-start">
                      <span class="font-bold mr-2">{{ replie.user.username }}:</span>
                      <span>{{ replie.content }}</span>
                      <div class="flex space-x-2" v-if="authStore.userID===replie.user.username ? true : false">
                        <button @click="putReplieId=replie.id; putContent=replie.content" class="btn btn-gray">수정</button>
                        <button @click="deleteComment(Article.id, replie.id)" class="btn btn-red">삭제</button>
                      </div>
                    </div>

                    <form v-on:submit.prevent="putComment(Article.id, replie.id, putContent,replie.user.username)"
                     v-if="putReplieId===replie.id" class="flex">
                      <input type="text" v-model="putContent" class="input">
                      <input type="submit" value="수정하기" class="btn btn-blue w-24">
                    </form>
                  </li>
                </ul>
              </details>
            </div>
          </li>
          <hr class="my-2">
        </ul>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import {getArticle, postComment, apiComment, deleteArticle, likeArticle} from '@/api/articleAPI'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const route = useRoute()
const router = useRouter()
const id = ref(route.params.id)
const authStore = useAuthStore()
const isLoading = ref(true)
const Article:any = ref(null)
const commentContent = ref('')
const putId = ref(null)
const putContent = ref('')
const replieContent = ref('')
const putReplieId = ref(null)
const isLike = ref(false)

const isWriter = computed(()=>{
  if(Article.value!==null){
    if(authStore.userID===Article.value.user.username) {
      return true
    }
  }
  return false
})


const Refresh = async (id:number) => {
  // router.go(0)
  // const response2 = await getArticle(id);
  // Article.value = response2;
  // 0.1초 후에 getArticle 함수를 실행
  setTimeout(async () => {
    const response2 = await getArticle(id);
    Article.value = response2;
  }, 100);
}
const likeArticleR =async (id:number) => {
  try{
    const result = await likeArticle(id)
    isLike.value = !isLike.value
    // Refresh(id)
  } catch {
    
  }
}
const deleteArticleR = async (id:number) => {
  try{
    const result = await deleteArticle(id)
    if (result){
      await router.push({path: "/article"})
    }
  } catch(error) {
    console.error(error);
  }
}

const postCommentR = async (id:number, content:string, parent=null) =>{
  if(content!==''){
    const result = await postComment(id,content, parent)
    commentContent.value=''
    replieContent.value=''
    await Refresh(id)
  }
}

const deleteComment =async (article_id:number,comment_id:number) => {
  await apiComment('delete', comment_id, '')
  await Refresh(article_id)
}

const putComment =async (article_id:number,comment_id:number, content:string, username:string) => {
  if (username===authStore.userID){
    await apiComment('put', comment_id, content)
    putContent.value = ''
    putId.value = null
    putReplieId.value = null
    await Refresh(article_id)
  } else {
    alert('권한이 없습니다.')
    // console.log('이름다름')
  }
}

onMounted(async () => {
  try {
    const article_id = Number(id.value)
    const response = await getArticle(article_id);
    Article.value = response;
    for(const like_user of Article.value.like_users){
      if(authStore.userID === like_user.username){
        isLike.value = true
      } else {
        isLike.value = false
      }
    }
    
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
});
</script>

<style scoped>
.btn {
  @apply font-bold py-2 px-4 rounded-full;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
.btn-red {
  @apply bg-red-500 text-white;
}
.btn-red:hover {
  @apply bg-red-700;
}
.btn-gray {
  @apply bg-gray-300 text-black;
}
.btn-gray:hover {
  @apply bg-gray-400;
}
.input{
  @apply w-full max-w-md;
}
</style>