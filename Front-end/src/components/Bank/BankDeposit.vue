<template>
  <article>
    <div class="flex justify-between items-center">
      <div>
        <label for="deposit">
          <input type="radio" name="Saving" id="deposit" checked
          v-model="radioValue.Saving" value="deposit">적금
        </label>
        <label for="saving">
          <input type="radio" name="Saving" id="saving"
          v-model="radioValue.Saving" value="saving">예금
        </label>
      </div>

      <div>
        <label for="intr_rate">
          <input type="radio" name="intr_rate" id="intr_rate" checked
          v-model="radioValue.sort_field" value="intr_rate">기본금리
        </label>
        <label for="intr_rate2">
          <input type="radio" name="intr_rate" id="intr_rate2"
          v-model="radioValue.sort_field" value="intr_rate2">우대금리
        </label>
      </div>

      <div>
        <label for="termAll">
          <input type="radio" name="term" id="termAll" checked
          v-model="radioValue.term" value="0">전체기간
        </label>
        <label for="term6">
          <input type="radio" name="term" id="term6"
          v-model="radioValue.term" value="6">6
        </label>
        <label for="term12">
          <input type="radio" name="term" id="term12"
          v-model="radioValue.term" value="12">12
        </label>
        <label for="term24">
          <input type="radio" name="term" id="term24"
          v-model="radioValue.term" value="24">24
        </label>
        <label for="term36">
          <input type="radio" name="term" id="term36"
          v-model="radioValue.term" value="36">36
        </label>
        <!-- <p>{{ radioValue }}</p> -->
      </div>

      <button @click="changeData" 
      class="bg-blue-500 hover:bg-blue-700 
      text-white font-bold py-2 px-4 rounded"
      >조회</button>
    </div>

    <div class="grid">
      <div class="grid grid-cols-8 bg-yellow-300 dark:bg-yellow-700 font-bold">
        <p class="p-2 col-span-3">상품명</p>
        <p class="p-2 col-span-1">금리</p>
        <p class="p-2 col-span-1">우대금리</p>
        <p class="p-2 col-span-1">기간</p>
        <p class="p-2 col-span-2">은행</p>
      </div>
      <div v-if="isLoading"> Loading...</div>
      <div v-else v-if="depositList">
        <ul v-for="deposit in depositList.results" class="bg-green-100 dark:bg-green-900">
          <li class="grid grid-cols-8" 
          @click="setModalOpen(deposit)">
            <span class="p-2 col-span-3">{{deposit.fin_prdt_cd.fin_prdt_nm}}</span>
            <span class="p-2 col-span-1">{{deposit.intr_rate}}</span>
            <span class="p-2 col-span-1">{{deposit.intr_rate2}}</span>
            <span class="p-2 col-span-1">{{deposit.save_trm}}</span>
            <span class="p-2 col-span-2">{{deposit.fin_prdt_cd.kor_co_nm}}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="isModalOpen.state"
    @click="setModalOpen(null)"
    class="modalBackground fixed top-0 left-0 z-10
    w-screen h-screen
    flex justify-center items-center">
      <div class="bg-white dark:bg-slate-600 absolute" @click.stop>
        <p>{{ isModalOpen.data?.fin_prdt_cd.fin_prdt_nm }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.kor_co_nm }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.etc_note }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.join_deny }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.join_member }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.join_way }}</p>
        <p>{{ isModalOpen.data?.fin_prdt_cd.spcl_cnd }}</p>
        <hr>
        <p>{{ isModalOpen.data?.intr_rate_type_nm }}</p>
        <p>{{ isModalOpen.data?.intr_rate }}</p>
        <p>{{ isModalOpen.data?.intr_rate2 }}</p>
        <p>{{ isModalOpen.data?.save_trm }}</p>
        <p>{{ isModalOpen.data?.rsrv_type }}</p>
        <p>{{ isModalOpen.data?.rsrv_type_nm }}</p>
      </div>
    </div>

  </article>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import getBankList from '../../api/bankDeposit';
import type {BankDataType, SavingType} from '@/interface/BankDataType'
const radioValue = ref({
  Saving: 'deposit',
  term:'0',
  sort_field: 'intr_rate'
})
const depositList = ref<BankDataType | null>(null);
const isLoading = ref(true);
const isModalOpen = ref({
  state: false,
  data: null as SavingType | null,
})
const setModalOpen = (deposit:SavingType|null) =>{
  isModalOpen.value.state = !isModalOpen.value.state
  if(isModalOpen.value.state){
    isModalOpen.value.data = deposit
  }
}

onMounted(async () => {
  try {
    const response = await getBankList();
    depositList.value = response;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
});

const changeData = async ()=>{
  try {
    const response = await getBankList(
                      radioValue.value.Saving
                      ,Number(radioValue.value.term)
                      ,radioValue.value.sort_field
                      );
    depositList.value = response;
  } catch (error) {
    console.error(error);
  }
}
</script>

<style scoped>
.modalBackground{
  background-color: rgb(0, 0, 0,0.5);
}
</style>