<template>
  <main class="grid grid-cols-12 gap-2 p-2 2xl:px-40">
    <KospiWeek class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <KosdaqWeek class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <GoldWeek class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <OilWeek class="col-span-12 sm:col-span-6 xl:col-span-3"/>

    <MainExchange class="col-span-12 sm:col-span-3 flex justify-center"/>
    <News class="col-span-12 sm:col-span-9  2xl:mx-9"/>
    
  </main>
</template>

<script setup lang="ts">
import KospiWeek from '@/components/Home/KospiWeek.vue';
import KosdaqWeek from '@/components/Home/KosdaqWeek.vue';
import GoldWeek from '@/components/Home/GoldWeek.vue';
import OilWeek from '@/components/Home/OilWeek.vue';
import MainExchange from '@/components/Home/MainExchange.vue';
import News from '@/components/Home/News.vue';
</script>

<style scoped>

</style>