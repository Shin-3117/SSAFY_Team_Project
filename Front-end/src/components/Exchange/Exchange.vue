<template>
  <div class="grid rounded-xl border-2 p-2 temp mt-4 border-indigo-400 animate-fade animate-duration-[1000ms]">
    <!-- Column Headers -->
    <div class="card font-bold grid grid-cols-7 gap-6 bg-indigo-400">
      <span class="col-span-3">외화</span>
      <span class="col-span-2">가격</span>
      <!-- <span class="col-span-2">1000원 당 외화</span> -->
      <span class="col-span-2">기준일자</span>
    </div>

    <!-- Exchange Data Items -->
    <div class="overflow-auto">
    <div v-for="data in exchangeData" :key="data.id" @click="reset(data.id)"
    class="card grid grid-cols-7 gap-6 hover:bg-indigo-400 dark:bg-indigo-500"
    :class="{ 'bg-indigo-300 dark:bg-indigo-700': isSelect===data.id }">
      <span class="col-span-3">{{ data.cur_unit }} - {{ data.cur_nm }}</span>
      <span class="col-span-2 font-extrabold text-lg">{{ parseFloat(data.deal_bas_r).toFixed(2) }}</span>
      <!-- <span class="col-span-2">{{ (data.krw_to_cur*1000).toFixed(2)}}</span> -->
      <span class="col-span-2">{{ data.req_dt }}</span>
      
      <div v-if="isSelect===data.id" class="col-span-7">
        <form @submit.prevent="exChange(data.deal_bas_r,1)" v-if="isSelect===data.id"
        class="flex">
          <label for="fm">외화 -> 원화
            <input type="number" id="fm" placeholder=" $ -> \" v-model="money">
          </label>
          <input type="submit" value="계산하기" class="hover:bg-indigo-600 font-extrabold animate-jump">
          <p class="ml-2 font-extrabold text-lg animate-jump">{{ exMoney }} ￦</p>
        </form>
        <form @submit.prevent="exChange(data.krw_to_cur,2)" v-if="isSelect===data.id"
        class="flex">
          <label for="fm">원화 -> 외화
            <input type="number" id="fm" placeholder=" \ -> $" v-model="money2">
          </label>
          <input type="submit" value="계산하기" class="hover:bg-indigo-600 font-extrabold animate-jump">
          <p class="ml-2 font-extrabold text-lg animate-jump">{{ exMoney2 }} $</p>
        </form>
      </div>
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
const money = ref(null)
const money2 = ref(null)
const exMoney = ref(null)
const exMoney2 = ref(null)

const reset = (id) => {
  if (isSelect.value!==id){
    money.value = null;
    money2.value = null;
    exMoney.value = null;
    exMoney2.value = null;
  }
  isSelect.value = id
}

const exChange = (rate, i) => {
  const cnt = money.value * parseFloat(rate)
  const cnt2 = money2.value/1000 * parseFloat(rate)
  if (i===1){
    exMoney.value = cnt.toFixed(2)
  }
  if (i===2){
    exMoney2.value = cnt2.toFixed(2)
  }
}
onMounted(async () => {
  try {
    const response = await getExchange();
    exchangeData.value = response;
    // 정렬 로직 추가
    exchangeData.value.sort((a, b) => {
      const priorityCurrencies = ['USD', 'EUR', 'JPY', 'CNH'];
      let aPriority = priorityCurrencies.indexOf(a.cur_unit);
      let bPriority = priorityCurrencies.indexOf(b.cur_unit);

      aPriority = aPriority === -1 ? priorityCurrencies.length : aPriority;
      bPriority = bPriority === -1 ? priorityCurrencies.length : bPriority;

      return aPriority - bPriority;
    });
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

.temp{
  height: 720px;
}

/* WebKit browsers (Chrome, Safari) */
::-webkit-scrollbar {
  width: 10px; /* width of the scrollbar */

}

::-webkit-scrollbar-track {

}

::-webkit-scrollbar-thumb {
  @apply bg-gray-400; /* color of the scrollbar handle */
  border-radius: 6px; /* roundness of the scrollbar handle */
}
</style>