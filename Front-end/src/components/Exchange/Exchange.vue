<template>
  <div class="grid">
    <!-- Column Headers -->
    <div class="font-bold grid grid-cols-9 bg-slate-100 dark:bg-slate-900">
      <span class="col-span-3">외화</span>
      <span class="col-span-2">1외화 당 원화</span>
      <span class="col-span-2">1000원 당 외화</span>
      <span class="col-span-2">Date</span>
    </div>

    <!-- Exchange Data Items -->
    <div v-for="data in exchangeData" :key="data.id" 
    class="grid grid-cols-9 bg-slate-50 dark:bg-slate-950 hover:bg-gray-200 dark:hover:bg-gray-800">
      <span class="col-span-3">{{ data.cur_unit }} - {{ data.cur_nm }}</span>
      <span class="col-span-2">{{ data.deal_bas_r }}</span>
      <span class="col-span-2">{{ data.krw_to_cur*1000 }}</span>
      <span class="col-span-2">{{ data.req_dt }}</span>
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