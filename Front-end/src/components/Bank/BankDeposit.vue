<template>
  <article>
    <div class="flex justify-between items-center">
      <div>
        <label for="deposit" class="Radio" :class="{ 'active': radioValue.Saving === 'deposit' }">
          <input type="radio" name="Saving" id="deposit" checked
          v-model="radioValue.Saving" value="deposit" class="hidden">예금
        </label>
        <label for="saving" class="Radio" :class="{ 'active': radioValue.Saving === 'saving' }">
          <input type="radio" name="Saving" id="saving"
          v-model="radioValue.Saving" value="saving" class="hidden">적금
        </label>
      </div>

      <div>
        <label for="intr_rate" class="Radio" :class="{ 'active': radioValue.sort_field === 'intr_rate' }">
          <input type="radio" name="intr_rate" id="intr_rate" checked
          v-model="radioValue.sort_field" value="intr_rate" class="hidden">기본금리
        </label>
        <label for="intr_rate2" class="Radio" :class="{ 'active': radioValue.sort_field === 'intr_rate2' }">
          <input type="radio" name="intr_rate" id="intr_rate2"
          v-model="radioValue.sort_field" value="intr_rate2" class="hidden">우대금리
        </label>
      </div>

      <div>
        <label for="termAll" class="Radio" :class="{ 'active': radioValue.term === '0' }">
          <input type="radio" name="term" id="termAll" checked
          v-model="radioValue.term" value="0" class="hidden">전체기간
        </label>
        <label for="term6" class="Radio" :class="{ 'active': radioValue.term === '6' }">
          <input type="radio" name="term" id="term6"
          v-model="radioValue.term" value="6" class="hidden">6
        </label>
        <label for="term12" class="Radio" :class="{ 'active': radioValue.term === '12' }">
          <input type="radio" name="term" id="term12"
          v-model="radioValue.term" value="12" class="hidden">12
        </label>
        <label for="term24" class="Radio" :class="{ 'active': radioValue.term === '24' }">
          <input type="radio" name="term" id="term24"
          v-model="radioValue.term" value="24" class="hidden">24
        </label>
        <label for="term36" class="Radio" :class="{ 'active': radioValue.term === '36' }">
          <input type="radio" name="term" id="term36"
          v-model="radioValue.term" value="36" class="hidden">36
        </label>
        <!-- <p>{{ radioValue }}</p> -->
      </div>

      <button @click="changeData()" 
      class="bg-blue-500 hover:bg-blue-700 
      text-white font-bold py-2 px-4 rounded"
      >조회</button>
    </div>

    <div class="grid">
      <div class="grid grid-cols-8 bg-slate-100 dark:bg-slate-900 font-bold">
        <p class="p-2 col-span-3">상품명</p>
        <p class="p-2 col-span-1">금리</p>
        <p class="p-2 col-span-1">우대금리</p>
        <p class="p-2 col-span-1">기간</p>
        <p class="p-2 col-span-2">은행</p>
      </div>
      <div v-if="isLoading"> Loading...</div>
      <div v-else v-if="depositList">
        <ul v-for="deposit in depositList.results" 
        class="bg-slate-50 dark:bg-slate-950 hover:bg-gray-200 dark:hover:bg-gray-800">
          <li class="grid grid-cols-8" 
          @click="setModalOpen(deposit)">
            <span class="p-2 col-span-3">{{deposit.fin_prdt_cd.fin_prdt_nm}}
              <span v-if="deposit.is_subscribed">*</span>
            </span>
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
      <div class="bg-white dark:bg-slate-600 w-4/5 p-3" @click.stop>
        <div class="flex  items-center justify-between mb-4">
          <p>{{ isModalOpen.data?.fin_prdt_cd.kor_co_nm }}</p>
          <p class="font-bold text-lg">{{ isModalOpen.data.fin_prdt_cd.fin_prdt_nm }}</p>
          <div v-if="authStore.token!==null">
            <button v-if="isModalOpen.data?.rsrv_type" 
            @click="postSaving(
              isModalOpen.data.fin_prdt_cd.id
              ,isModalOpen.data.id
              ,currentPage
              ,currentPath
              ,token
              ).then(()=>{changeData()})"
            ><img src="@/assets/star-solid.svg" alt="star" class="w-6 h-6"></button>
            <button v-if="!isModalOpen.data?.rsrv_type"
            @click="postDeposit(
              isModalOpen.data.fin_prdt_cd.id
              ,isModalOpen.data.id
              ,currentPage
              ,currentPath
              ,token
              ).then(()=>{changeData()})"
            ><img src="@/assets/star-solid.svg" alt="star" class="iconImg"></button>
          </div>
        </div>
        <hr class="my-4">
        <div class="mb-4 flex">
          <p class="font-bold">가입 제한: {{ isModalOpen.data?.fin_prdt_cd.join_deny }}</p>
          <p class="ml-2 text-gray-500">1: 제한없음, 2: 서민전용, 3: 일부제한</p>
        </div>
        <p class="mb-4">가입 대상: {{ isModalOpen.data?.fin_prdt_cd.join_member }}</p>
        <p class="mb-4">가입 방법: {{ isModalOpen.data?.fin_prdt_cd.join_way }}</p>
        <p class="mb-4">우대조건: {{ isModalOpen.data?.fin_prdt_cd.spcl_cnd }}</p>
        <p class="mb-4 font-bold">기타 유의사항:</p>
        <p class="mb-4">{{ isModalOpen.data?.fin_prdt_cd.etc_note }}</p>
        <hr class="my-4">
        <p class="mb-4 font-bold">금리 적용 방식: {{ isModalOpen.data?.intr_rate_type_nm }}</p>
        <p class="mb-4">기본금리: {{ isModalOpen.data?.intr_rate }}</p>
        <p class="mb-4">우대금리: {{ isModalOpen.data?.intr_rate2 }}</p>
        <p class="mb-4">저축기간: {{ isModalOpen.data?.save_trm }}</p>
        <p class="mb-4">{{ isModalOpen.data?.rsrv_type }}</p>
        <p class="mb-4">{{ isModalOpen.data?.rsrv_type_nm }}</p>
        <hr class="my-4">
        <!-- <p>{{ isModalOpen.data?.is_subscribed }}</p> -->
        <!-- <p>{{ isModalOpen.data }}</p> -->
      </div>
    </div>
    
  <div v-if="depositList">
    <ul class="flex justify-center items-center space-x-2 bg-slate-50 dark:bg-slate-950">
      <li
        v-for="page in pageNation"
        :key="page"
        @click="setPage(page)"
        :class="{ 'bg-gray-500 text-white': page === currentPage }"
        class="px-3 py-2 cursor-pointer border border-gray-300 rounded-md
        hover:bg-gray-200 dark:hover:bg-gray-800 "
      >
        {{ page }}
      </li>
    </ul>
  </div>

  </article>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type {BankDataType, SavingType} from '@/interface/BankDataType'
import {getBankList, postDeposit, postSaving} from '../../api/bankDeposit';
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore()
const radioValue = ref({
  Saving: 'deposit',
  term:'0',
  sort_field: 'intr_rate'
})
const depositList = ref<BankDataType | null>(null);
const isLoading = ref(true);
const currentPage = ref(1)
const currentPath = ref('')
const pageNation = ref<number[]>([])
const token = authStore.token

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
const setPage = (page:number) => {
  currentPage.value = page
  changeData()
}
const changeData = async ()=>{
  isLoading.value = true
  try {
    const response = await getBankList(
                      radioValue.value.Saving
                      ,radioValue.value.term
                      ,radioValue.value.sort_field
                      ,currentPage.value
                      ,token
                      );
    depositList.value = response;
    pageNation.value = []
    if(depositList.value!==null){
      const totalPage = depositList.value.count
      for (let i=1; i-1<totalPage/20; i++){
        pageNation.value.push(i)
      }
    }
    currentPage.value = response.page
    currentPath.value = response.path
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false
  }
}
onMounted(async () => {
  changeData()
});
</script>

<style scoped>
.modalBackground{
  background-color: rgb(0, 0, 0,0.5);
}
.Radio{
  @apply cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-blue-600 hover:bg-blue-700
}
.iconImg{
  width: 24px;
  height: 24px;
  fill: #FFEA00;
}
</style>