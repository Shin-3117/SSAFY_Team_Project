<template>
  <section v-if="news" class="card h-96">
    <h2  class="font-bold text-center pb-2">경제 뉴스</h2>
    <ul class="h-80 overflow-y-auto">
      <li v-for="ne in news">
        <a :href="ne.originallink" target="_blank" rel="noreferrer noopener"
        class="card flex justify-start">
        <p class="whitespace-nowrap mr-2">{{ ne.pubdate }}</p>
        <p class="truncate">{{ ne.title }}</p>
        </a>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import getNews from '@/api/NewAPI'
import { onMounted, ref } from 'vue';

const news = ref()
onMounted( async ()=>{
  const response = await getNews()
  news.value = response
})
</script>

<style scoped>
.card{
  @apply rounded-xl border p-2;
}
/* WebKit browsers (Chrome, Safari) */
::-webkit-scrollbar {
  width: 12px; /* width of the scrollbar */

}

::-webkit-scrollbar-track {

}

::-webkit-scrollbar-thumb {
  background-color: rgba(128, 128, 128, 0.5); /* color of the scrollbar handle */
  border-radius: 6px; /* roundness of the scrollbar handle */
}

::-webkit-scrollbar-thumb:hover {
  background-color: gold; /* color of the scrollbar handle on hover */
}
</style>