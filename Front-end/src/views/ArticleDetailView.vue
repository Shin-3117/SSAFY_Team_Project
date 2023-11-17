<template>
  <main>
    <div class="border border-slate-600" v-if="Article">
      <h2>{{ Article.title }}</h2>
      <RouterLink to="/article">게시판으로</RouterLink>
      <br>
      <RouterLink :to="`/article/${Article.id}/put`">수정하기</RouterLink>
      <button @click="deleteArticleR(Article.id)">삭제</button>
      <br>
      <span>작성자: {{ Article.user.username }} |</span>
      <span>{{ Article.updated_at }}</span>
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
            <button @click="putId=comment.id">수정</button>
            <div v-if="putId===comment.id">
              <input type="text" :placeholder="comment.content" v-model="putContent">
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
  <button @click="putReplieId=replie.id">수정</button>
  <div v-if="putReplieId===replie.id">
    <input type="text" :placeholder="replie.content" v-model="putContent">
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
import {getArticle, postComment, apiComment, deleteArticle} from '@/api/articleAPI'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

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

const Refresh = async (id:number) => {
    const response2 = await getArticle(id);
    Article.value = response2;
}

const deleteArticleR = async (id:number) => {
  try{
    const result = await deleteArticle(id)
    if (result){
      await router.push({path: "/article"})
    }
  } catch {
    
  }
}

const postCommentR = async (id:number, content:string, parent=null) =>{
  if(content!==''){
    await postComment(id,content, parent)
    Refresh(id)
  }
}

const deleteComment =async (article_id:number,comment_id:number) => {
  apiComment('delete', comment_id, '')
  Refresh(article_id)
}

const putComment =async (article_id:number,comment_id:number, content:string, username:string) => {
  if (username===authStore.userID){
    apiComment('put', comment_id, content)
    putContent.value = ''
    putId.value = null
    putReplieId.value = null
    Refresh(article_id)
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

</style>