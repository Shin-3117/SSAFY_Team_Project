<template>
  <div>
    <div class="flex flex-col">
      <label for="title">제목
      </label>
      <input type="text" id="title" v-model="title"
      class="border border-teal-100">
      <textarea v-model="content" rows="7" 
      class="border border-teal-100"></textarea>
      <!-- <p>{{ content }}</p> -->
      <button @click="moveArticles()">뒤로가기</button>
      <button @click="MakeArticle(title, content)">게시글 생성하기</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {postArticle} from '@/api/articleAPI'
import { useRouter } from "vue-router";

const router = useRouter()
const title = ref('')
const content = ref('')

const moveArticles = () => {
  router.push({path: "/article"})
}

const MakeArticle = async (title:string, content:string) => {
  try{
    const toHTML = content.replaceAll(/(\n|\r\n)/g,'<br>')
    const response = await postArticle(title, toHTML)
    if (response){
      await router.push({path: "/article"})
    }
  } catch(error){
    console.error(error)
  }
}

</script>

<style scoped>
.contentBox{
  border: 1px solid;
  widows: 500px;
  height: 300px;
}
</style>