<template>
  <div>
    {{exchangeData}}
  </div>
</template>

<script setup lang="ts">
import getExchange from '@/api/Exchange'
import { ref, onMounted } from 'vue';

const exchangeData = ref(null);
const isLoading = ref(true);
onMounted(async () => {
  try {
    const response = await getExchange();
    exchangeData.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
});
</script>

<style scoped>

</style>