<template>
  <main>
    <div class="border border-slate-600" v-if="Article">
      <h2>{{ Article.title }}</h2>
      <RouterLink to="/article">게시판으로</RouterLink>
      <br>
      <div v-if="isWriter">
        <RouterLink :to="`/article/${Article.id}/put`">수정하기</RouterLink>
        <button @click="deleteArticleR(Article.id)">삭제</button>
      </div>
      <button @click="likeArticleR(Article.id)">좋아요</button>
      <br>
      <span>작성자: {{ Article.user.username }} | </span>
      <span>{{ Article.updated_at }} | </span>
      <RouterLink :to="`/userInfo/${Article.user.username}`" class="btn btn-blue"
      >작성자정보</RouterLink>
      <div v-html="Article.content"></div>
      <br><hr>
      <form v-on:submit.prevent="postCommentR(Article.id, commentContent)">
        <label for="content">댓글작성 :
          <input type="text" id="content" v-model="commentContent"
           class="border border-stone-600">
        </label>
        <input type="submit" value="제출하기">
      </form>
      
      <div v-if="Article.comments">
        <p>댓글 {{ Article.comments.length }}</p>
        <hr>
        <ul v-for="comment in Article.comments" :key="comment.id">
          <li>
            <p>{{ comment.user.username }}</p>
            <p>{{ comment.content }}</p>
            <button @click="()=>{putId=comment.id; putContent=comment.content}">수정</button>
            <div v-if="putId===comment.id">
              <input type="text" v-model="putContent">
              <button @click="putComment(Article.id, comment.id, putContent,comment.user.username)">수정하기</button>
            </div>
            <button @click="deleteComment(Article.id, comment.id)"> 삭제</button>
            <details v-if="comment.replies">
              <summary> 
                <span>대댓글 {{ comment.replies.length }} | </span>
              </summary>
              <input type="text" class="border border-lime-300" v-model="replieContent">
              <button @click="postCommentR(Article.id, replieContent, comment.id)">대댓글 작성</button>
                <ul v-for="replie in comment.replies">
                  <li>
                    <span>ㄴ{{ replie.user.username }}: </span>
                    <span>{{ replie.content }}</span>
  <button @click="putReplieId=replie.id; putContent=replie.content">수정</button>
  <div v-if="putReplieId===replie.id">
    <input type="text" v-model="putContent">
    <button @click="putComment(Article.id, replie.id, putContent,replie.user.username)">수정하기</button>
  </div>
  <button @click="deleteComment(Article.id, replie.id)"> 삭제</button>
                  </li>
                </ul>
            </details>
          </li>
          <hr>
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
    // console.log(result)
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
</style>