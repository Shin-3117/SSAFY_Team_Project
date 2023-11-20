<template>
  <div class="grid">
    <!-- Column Headers -->
    <div class="font-bold flex justify-between p-2 border-b">
      <span class="">Currency</span>
      <span class="mr-10">Rate</span>
      <span class="mr-10">Exchange Rate</span>
      <span>Date</span>
    </div>

    <!-- Exchange Data Items -->
    <div v-for="data in exchangeData" :key="data.id" class="flex justify-between p-2 border-b">
      <span class="">{{ data.cur_unit }} - {{ data.cur_nm }}</span>
      <span class="mr-10">{{ data.deal_bas_r }}</span>
      <span class="mr-10">{{ data.krw_to_cur }}</span>
      <span>{{ data.req_dt }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import getExchange from '@/api/Exchange'
import { ref, onMounted } from 'vue';
import type ExchangeType from '@/interface/ExchangeType';
const exchangeData = ref<ExchangeType[]|null>(null);
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