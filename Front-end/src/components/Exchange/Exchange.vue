<template>
  <div class="grid card">
    <!-- Column Headers -->
    <div class="card font-bold grid grid-cols-7 gap-6 bg-slate-100 dark:bg-slate-900">
      <span class="col-span-3">외화</span>
      <span class="col-span-2">가격</span>
      <!-- <span class="col-span-2">1000원 당 외화</span> -->
      <span class="col-span-2">Date</span>
    </div>

    <!-- Exchange Data Items -->
    <div v-for="data in exchangeData" :key="data.id" @click="reset(data.id)"
    class="card grid grid-cols-7 gap-6 bg-slate-50 dark:bg-slate-950 hover:bg-gray-200 dark:hover:bg-gray-800">
      <span class="col-span-3">{{ data.cur_unit }} - {{ data.cur_nm }}</span>
      <span class="col-span-2">{{ data.deal_bas_r }}</span>
      <!-- <span class="col-span-2">{{ (data.krw_to_cur*1000).toFixed(2)}}</span> -->
      <span class="col-span-2">{{ data.req_dt }}</span>
      
      <div v-if="isSelect===data.id" class="col-span-7">
        <form @submit.prevent="exChange(data.deal_bas_r,1)" v-if="isSelect===data.id"
        class="flex">
          <label for="fm">외화 당 원화
            <input type="number" id="fm" placeholder=" \ -> $" v-model="money">
          </label>
          <input type="submit" value="계산하기">
          <p class="ml-2">{{ exMoney }} ￦</p>
        </form>
        <form @submit.prevent="exChange(data.krw_to_cur,2)" v-if="isSelect===data.id"
        class="flex">
          <label for="fm">원화 당 외화
            <input type="number" id="fm" placeholder=" \ -> $" v-model="money2">
          </label>
          <input type="submit" value="계산하기">
          <p class="ml-2">{{ exMoney2 }} $</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import getExchange from '@/api/Exchange'
import { ref, onMounted } from 'vue';
import type ExchangeType from '@/interface/ExchangeType';
const exchangeData = ref<ExchangeType[]|null>(null);
const isLoading = ref(true);
const isSelect = ref(23)
const money = ref(1)
const money2 = ref(1000)
const exMoney = ref(0)
const exMoney2 = ref(0)

const reset = (id) => {
  if (isSelect.value!==id){
    money.value = 1
    money2.value = 1000
    exMoney.value = 0
    exMoney2.value = 0
  }
  isSelect.value = id
}

const exChange = (rate, i) => {
  const cnt = money.value * parseFloat(rate)
  if (i===1){
    exMoney.value = cnt.toFixed(2)
  }
  if (i===2){
    exMoney2.value = cnt.toFixed(2)
  }
}
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
.card{
  @apply rounded-xl border p-2;
}
</style>