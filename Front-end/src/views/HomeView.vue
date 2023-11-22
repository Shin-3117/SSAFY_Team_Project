<template>
  <main class="grid grid-cols-12 gap-3 p-2 lg:p-4" class="flex justify-center">
    <MainExchange class="col-span-12 sm:col-span-3 xl:col-span-2 xl:col-start-2"/>
    <News class="sm:col-span-9 col-span-12 xl:col-span-8"/>
    
    <Kospi />
    <kosdaq />
    <gold />
    <oil />
  </main>
</template>

<script setup lang="ts">
import Kospi from '@/components/testHome/kospi.vue';
import kosdaq from '@/components/testHome/kosdaq.vue';
import gold from '@/components/testHome/gold.vue';
import oil from '@/components/testHome/oil.vue';
import MainExchange from '@/components/Home/MainExchange.vue';
import News from '@/components/Home/News.vue';
</script>

<style scoped>

</style>