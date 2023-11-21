<template>
  <div>
    <div class="flex flex-col p-4">
      <label for="title">제목
      </label>
      <input type="text" id="title" v-model="title"
      class="mb-4">
      <textarea v-model="content" rows="7" 
      class="border border-slate-500 dark:bg-slate-900"></textarea>

      <button @click="moveArticles()">뒤로가기</button>
      <button @click="MakeArticle(title, content)">게시글 수정하기</button>
    </div>
    <!-- <p>{{ Article }}</p> -->
  </div>
</template>

<script setup lang="ts">
import {getArticle, putArticle} from '@/api/articleAPI'
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from "vue-router";

const Article:any = ref(null)
const route = useRoute()
const id = ref(route.params.id)
const router = useRouter()
const title = ref('')
const content = ref('')

const moveArticles = () => {
  router.push({path: `/article/${id.value}`})
}

const MakeArticle = async (title:string, content:string) => {
  try{
    const toHTML = content.replaceAll(/(\n|\r\n)/g,'<br>')
    const response = await putArticle(id.value,title, toHTML)
    if (response){
      await router.push({path: `/article/${id.value}`})
    }
  } catch(error){
    console.error(error)
  }
}

onMounted(async () => {
  try {
    const article_id = Number(id.value)
    const response = await getArticle(article_id);
    Article.value = response;
    title.value = Article.value.title
    content.value = Article.value.content.replaceAll('<br>','\n')
  } catch (error) {
    console.error(error);
  }
});
</script>

<style scoped>
.contentBox{
  border: 1px solid;
  widows: 500px;
  height: 300px;
}
</style>