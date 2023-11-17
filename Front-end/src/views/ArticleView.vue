<template>
  <main>
    <h1>Atricle</h1>
    <RouterLink to="/article/post">게시판 작성</RouterLink>
    <div v-if="isLoading">Loading...</div>
    <section v-else>
      <ul v-for="article in Articles" :key="article.id">
        <RouterLink :to="`/article/${article.id}`">
          <li>
            <span>{{ article.title }} | </span>
            <span>작성자: {{ article.user.username }}</span>
          </li>
        </RouterLink>
      </ul>
    </section>
    <br>
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