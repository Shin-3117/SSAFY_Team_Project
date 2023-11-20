<template>
  <main>
    <h1>Atricle</h1>
    <RouterLink to="/article/post">게시판 작성</RouterLink>
    <section class="grid">
      <div class="grid grid-cols-8">
        <p class="col-span-4">제목</p>
        <p class="col-span-1">작성자</p>
        <p class="col-span-3">작성일</p>
      </div>
      <hr>
      <div v-if="isLoading">Loading...</div>
      <div v-else>
        <ul v-for="article in Articles" :key="article.id">
          <RouterLink :to="`/article/${article.id}`">
            <li class="grid grid-cols-8">
              <p class="col-span-4">{{ article.title }} | </p>
              <p class="col-span-1">{{ article.user.username }}</p>
              <p class="col-span-3">{{ article.created_at }}</p>
            </li>
          </RouterLink>
        </ul>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import {getArticles, getArticle, postComment} from '@/api/articleAPI'
import { ref, onMounted } from 'vue'
import type {ArticlesType} from '@/interface/ArticlesType'

const isLoading = ref(true)
const Articles = ref<ArticlesType[] | null>(null)

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

</style>