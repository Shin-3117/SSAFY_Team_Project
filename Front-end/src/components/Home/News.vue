<template>
  <section v-if="news" class="sectionContainer h-96">
    <h2  class="font-bold text-center pb-2">경제 뉴스</h2>
    <ul class="h-80 overflow-y-auto">
      <li v-for="ne in news" class="hover:bg-indigo-200">
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
.sectionContainer{
  @apply border-4 rounded-xl p-2 border-slate-500;
}
.card{
  @apply rounded-xl border-2 p-2 border-slate-500;
}
/* WebKit browsers (Chrome, Safari) */
::-webkit-scrollbar {
  width: 10px; /* width of the scrollbar */

}

::-webkit-scrollbar-track {

}

::-webkit-scrollbar-thumb {
  @apply bg-gray-400; /* color of the scrollbar handle */
  border-radius: 6px; /* roundness of the scrollbar handle */
}
</style>