<template>
  <div class="grid grid-cols-12 gap-3 p-2 lg:p-4">
    <h2 class="col-span-12">Home</h2>
    <MainExchange class="col-span-12 sm:col-span-3 xl:col-span-2"/>
    <News class="sm:col-span-9 col-span-12 xl:col-span-10"/>
  </div>
</template>

<script setup lang="ts">
import MainExchange from '@/components/Home/MainExchange.vue';
import News from '@/components/Home/News.vue';
</script>

<style scoped>

</style>