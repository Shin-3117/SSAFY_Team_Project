<template>
  <div>
    <!-- <div v-if="exchangeData">
    <div class="bg-lime-300">
      <h2>환율 계산하기</h2><hr>
      <label for="wonTo">외화로 바꾸기</label>
      <input type="number" name="" id="wonTo" v-model="foreignCurrency"
      class="border border-slate-300 hover:border-indigo-300">
      <p>{{ parseFloat(exchangeData[22].cur_nm) }}</p>
      <br>
      <label for="wonTo">원화로 바꾸기</label>
      <input type="number" name="" id="wonTo" v-model="nationalCurrency"
      class="border border-slate-300 hover:border-indigo-300">
    </div>

      <span>{{ exchangeData[22].cur_nm }} | </span>
      <span>{{ exchangeData[22].deal_bas_r }}\ | </span>
      <span>1000\ -> {{ exchangeData[22].krw_to_cur }}</span>
    </div> -->
    <!-- {{exchangeData}} -->
    <button @click="findCountry(countryCode)">USD</button>
    <div v-if="eachExchangeData">
      <p>{{ eachExchangeData }}</p>
      <input type="number" name="" id="" v-model="foreignCurrency">
      <p>{{ (eachExchangeData.deal_bas_r*foreignCurrency).toFixed(2) }}</p>

      <input type="number" name="" id="" v-model="nationalCurrency">천원
      <p>{{ (eachExchangeData.krw_to_cur*nationalCurrency).toFixed(2) }}</p>
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

const countryCode = ref('USD')
const eachExchangeData = ref<ExchangeType|null>(null);
const findCountry = (CUR:string) => {
  if (exchangeData.value!==null){
    for (const ex of exchangeData.value){
      if(ex.cur_unit===CUR){
        eachExchangeData.value = ex
        eachExchangeData.value.deal_bas_r = parseFloat(eachExchangeData.value.deal_bas_r)
        eachExchangeData.value.krw_to_cur = parseFloat(eachExchangeData.value.krw_to_cur)
      }
    }
  }
}

const foreignCurrency = ref(1)
const nationalCurrency = ref(1)
</script>

<style scoped>

</style>