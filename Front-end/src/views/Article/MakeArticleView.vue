<template>
  <div class="animate-fade-left animate-once animate-duration-1000">
    <div class="flex flex-col p-4 w-2/4 m-auto">
      <label for="title" class="text-xl font-semibold">제목
        <input type="text" id="title" v-model="title"
        class="mb-4 w-full rounded-lg">
      </label>
      <div class="text-xl font-semibold">내용</div>
      <textarea v-model="content" rows="7" 
      class="border border-slate-500 dark:bg-slate-900 rounded-lg p-4"></textarea>
      <!-- <p>{{ content }}</p> -->
      <div class="flex justify-center mt-4 gap-4"><button @click="moveArticles()" class="Radio">뒤로가기</button>
      <button @click="MakeArticle(title, content)" class="Radio">게시글 생성하기</button></div>
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

.Radio{
  @apply cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 
  text-white font-bold py-2 px-4 rounded-full mr-1;
}
</style>