<template>
<article>
  <div v-if="isLoading">
    Loading...
  </div>
  
<div v-if="!isLoading" class="container">
  <h2 class="font-bold text-center">
    <RouterLink to="/ExchangeRate">주요 국가 환율</RouterLink>
  </h2>
  <div class="flex sm:flex-col">  
    <div class="card max-h-44 my-2">
      <!-- {{ USDData }} -->
      <img src="@/assets/img/flag/Flag_of_the_United_States.svg" alt="미국기"
        class="flagImg border-2 border-black">
      <p class="font-bold">1달러 = {{ USDData?.deal_bas_r }} 원</p>
    </div>
    <div class="card ">
      <!-- {{ JPYData }} -->
      <img src="@/assets/img/flag/Flag_of_Japan.svg" alt="일장기"
      class="flagImg border-2 border-black">
      <p class="font-bold">100엔 = {{ JPYData?.deal_bas_r*100 }} 원</p>
    </div>
  </div>
</div>
</article>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import getExchange from '@/api/Exchange'
import type ExchangeType from '@/interface/ExchangeType';

const USDData = ref<ExchangeType|null>(null);
const JPYData = ref<ExchangeType|null>(null);
const isLoading = ref(true);

onMounted(async () => {
  try {
    const responseUSD = await getExchange('USD');
    USDData.value = responseUSD;

    const responseJPY = await getExchange('JPY');
    JPYData.value = responseJPY;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.container{
  @apply border-4 rounded-xl p-2 border-slate-500
  flex flex-col justify-center items-center
  max-h-96 max-w-fit;
}
.card{
  @apply rounded-xl border-2 p-2 flex flex-col justify-center items-center border-slate-500;
}
.flagImg{
  max-height: 120px;
}
</style>