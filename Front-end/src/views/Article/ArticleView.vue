<template>
<main class="p-4 animate-fade-right animate-once animate-duration-1000">
  <article class="mx-auto w-2/4">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-bold mb-4">게시판</h2>
      <div v-if="authStore.token!==null">
        <RouterLink to="/article/post"
        class="Radio">게시글 작성</RouterLink>
      </div>
      <div v-else>
        로그인 후, 게시글 작성이 가능합니다.
      </div>
    </div>
    <section>
      <div class="grid grid-cols-9 bg-indigo-200 rounded-xl dark:bg-gray-900 p-2">
        <p class="col-span-5">제목</p>
        <p class="col-span-2">작성자</p>
        <p class="col-span-2">작성일</p>
      </div>
      <div v-if="isLoading" class="text-center">Loading...</div>
      <div v-else>
        <ul>
          <RouterLink v-for="article in Articles" :key="article.id" :to="`/article/${article.id}`">
            <li class="grid grid-cols-9 p-2 bg-slate-50 dark:bg-slate-950 hover:bg-gray-200 dark:hover:bg-gray-800">
              <p class="col-span-5">{{ article.title }}</p>
              <p class="col-span-2">{{ article.user.username }}</p>
              <p class="col-span-2">{{ article.created_at.slice(0, 10) }}</p>
            </li>
          </RouterLink>
        </ul>
      </div>
    </section>
  </article>
</main>
</template>

<script setup lang="ts">
import {getArticles, getArticle, postComment} from '@/api/articleAPI'
import { ref, onMounted } from 'vue'
import type {ArticlesType} from '@/interface/ArticlesType'
import { useAuthStore } from '../../stores/auth';

const isLoading = ref(true)
const Articles = ref<ArticlesType[] | null>(null)
const authStore = useAuthStore()

onMounted(async () => {
  try {
    const response = await getArticles();
    Articles.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
});

</script>

<style scoped>
.Radio{
  @apply cursor-pointer bg-indigo-500 hover:bg-gradient-to-br from-purple-700 to-blue-600 
  text-white font-bold py-2 px-4 rounded-full mr-1;
}
</style>