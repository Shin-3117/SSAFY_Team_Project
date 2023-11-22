<template>
  <div>
    Home
    <Kospi />
    <kosdaq />
    <gold />
    <oil />
  </div>
</template>

<script setup lang="ts">
import Kospi from '@/components/testHome/kospi.vue';
import kosdaq from '@/components/testHome/kosdaq.vue';
import gold from '@/components/testHome/gold.vue';
import oil from '@/components/testHome/oil.vue';

</script>

<style scoped>

</style>