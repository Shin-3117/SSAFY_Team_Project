<template>
  <main class="grid grid-cols-12 gap-2 p-2 2xl:px-40">
    <Kospi class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <kosdaq class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <gold class="col-span-12 sm:col-span-6 xl:col-span-3"/>
    <oil class="col-span-12 sm:col-span-6 xl:col-span-3"/>

    <MainExchange class="col-span-12 sm:col-span-3 flex justify-center"/>
    <News class="col-span-12 sm:col-span-9  2xl:mx-9"/>
    
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