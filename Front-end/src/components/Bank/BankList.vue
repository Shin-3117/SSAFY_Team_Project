<template>
  <article class="wrap px-4 rounded-xl border-2 border-indigo-400 py-2 my-4 animate-fade animate-duration-[1000ms]">
    <div class="flex justify-between items-center card bg-indigo-200">
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
      class="bg-gradient-to-br from-purple-600 to-blue-500 
  text-white font-bold py-2 px-4 rounded-md mr-1"
      >조회</button>
    </div>

    <div class="grid card">
      <div class="grid grid-cols-8 dark:bg-slate-900 font-bold rounded-xl temp2 bg-indigo-200">
        <p class="p-2 col-span-3">상품명</p>
        <p class="p-2 col-span-1 table"
        :class="{ 'font-bold bg-indigo-300': isNormalRate }">금리</p>
        <p class="p-2 col-span-1 table"
        :class="{ 'font-bold bg-indigo-300': !isNormalRate }">우대금리</p>
        <p class="p-2 col-span-1 table">기간</p>
        <p class="p-2 col-span-2 table">은행</p>
      </div>
      <div v-if="isLoading"> Loading...</div>
      <div v-else v-if="depositList"
      class="overflow-auto temp">
        <ul v-for="deposit in depositList.results" 
        class="bg-slate-50 dark:bg-slate-950 hover:bg-indigo-200 dark:hover:bg-gray-800 rounded-xl">
          <li class="grid grid-cols-8" 
          @click="setModalOpen(deposit)">
            <span class="p-2 col-span-3 flex">{{deposit.fin_prdt_cd.fin_prdt_nm}}
              <img v-if="deposit.is_subscribed" src="@/assets/img/star-fill.png" alt="star" class="iconImg">
            </span>
            <span class="p-2 col-span-1 table"
            :class="{ 'font-bold': isNormalRate }">{{deposit.intr_rate}}</span>
            <span class="p-2 col-span-1 table"
            :class="{ 'font-bold': !isNormalRate }">{{deposit.intr_rate2}}</span>
            <span class="p-2 col-span-1 table">{{deposit.save_trm}}</span>
            <span class="p-2 col-span-2 table">{{deposit.fin_prdt_cd.kor_co_nm}}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="isModalOpen.state"
    @click="setModalOpen(null)"
    class="modalBackground fixed top-0 left-0 z-10
    w-screen h-screen
    flex justify-center items-center">
      <div class="bg-white dark:bg-slate-600 w-4/5 p-3 border-4 border-indigo-400 animate-fade" @click.stop>
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
              ).then(()=>{
                isModalOpen.subscribe = !isModalOpen.subscribe
                changeData()})">
              <img v-if="isModalOpen.subscribe" src="@/assets/img/star-fill.png" alt="star" class="iconImg">
              <img v-if="!isModalOpen.subscribe" src="@/assets/img/star-null.png" alt="star" class="iconImg">
            </button>
            
            <button v-if="!isModalOpen.data?.rsrv_type"
            @click="postDeposit(
              isModalOpen.data.fin_prdt_cd.id
              ,isModalOpen.data.id
              ,currentPage
              ,currentPath
              ,token
              ).then(()=>{
                isModalOpen.subscribe = !isModalOpen.subscribe
                changeData()})">
              <img v-if="isModalOpen.subscribe" src="@/assets/img/star-fill.png" alt="star" class="iconImg">
              <img v-if="!isModalOpen.subscribe" src="@/assets/img/star-null.png" alt="star" class="iconImg">
            </button>
          </div>
        </div>
        <hr class="my-4">
        <div class="mb-4 flex">
          <p class="font-bold">가입 제한: {{ isModalOpen.data?.fin_prdt_cd.join_deny }}</p>
          <p class="ml-2 text-gray-500">1: 제한없음, 2: 서민전용, 3: 일부제한</p>
        </div>
        <div class="flex flex-col text-start  gap-4">
          <p class="font-bold">금리 적용 방식: {{ isModalOpen.data?.intr_rate_type_nm }}</p>
          <div class="flex gap-4">
            <p class="">기본금리: {{ isModalOpen.data?.intr_rate }}</p>
            <p class="">우대금리: {{ isModalOpen.data?.intr_rate2 }}</p>
            <p class="">저축기간: {{ isModalOpen.data?.save_trm }}</p>
            <p class="">{{ isModalOpen.data?.rsrv_type_nm }}</p>
          </div>
          <p class="">가입 대상: {{ isModalOpen.data?.fin_prdt_cd.join_member }}</p>
          <p class="">가입 방법: {{ isModalOpen.data?.fin_prdt_cd.join_way }}</p>
          <hr>
          <p class="">우대조건: 
            <p class="">{{ isModalOpen.data?.fin_prdt_cd.spcl_cnd }}</p>
          </p>
          <p class=" font-bold">기타 유의사항:</p>
          <p class="">{{ isModalOpen.data?.fin_prdt_cd.etc_note }}</p>
          
        </div>
        <!-- <p>{{ isModalOpen.data?.is_subscribed }}</p> -->
        <!-- <p>{{ isModalOpen.data }}</p> -->
      </div>
    </div>
    
  <div v-if="depositList">
    <ul class="flex justify-center items-center space-x-2 dark:bg-slate-950 rounded-xl bg-indigo-200">
      <li
        v-for="page in pageNation"
        :key="page"
        @click="setPage(page)"
        :class="{ 'bg-indigo-500 text-white': page === currentPage }"
        class="px-4 py-2 cursor-pointer border border-gray-300 rounded-xl bg-indigo-100
        hover:bg-indigo-400 dark:hover:bg-gray-800 my-2"
      >
        {{ page }}
      </li>
    </ul>
  </div>
  </article>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
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
const currentPath = ref('n/')
const pageNation = ref<number[]>([])
const token = authStore.token

const isModalOpen = ref({
  state: false,
  data: null as SavingType | null,
  subscribe: false
})

const isNormalRate = computed(()=>{
  if(currentPath.value.charAt(currentPath.value.length-2)==='2'){
    return false
  } else {
    return true
  }
})

const setModalOpen = (deposit:SavingType|null) =>{
  isModalOpen.value.state = !isModalOpen.value.state
  if(isModalOpen.value.state){
    isModalOpen.value.data = deposit
  }
  if(deposit?.is_subscribed===true){
    isModalOpen.value.subscribe = deposit?.is_subscribed
  }else{
    isModalOpen.value.subscribe = false
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
.wrap{
  width: 80%;
  min-width: 820px;
  max-width: 1200px;
}
.modalBackground{
  background-color: rgb(0, 0, 0,0.5);
}
.Radio{
  @apply cursor-pointer bg-indigo-400 hover:bg-gradient-to-br from-purple-600 to-blue-500 
  text-white font-bold py-2 px-4 rounded-md mr-1;
}
.Radio.active {
  @apply bg-gradient-to-br from-purple-600 to-blue-500 border-4 border-indigo-500;
}
.iconImg{
  width: 24px;
  height: 24px;
  fill: #FFEA00;
}
.table{
  border-left: solid;
  @apply border-indigo-200;
}
.card{
  @apply rounded-xl border p-2;
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

.temp{
  height: 620px;
}
.temp2{
  margin-right: 10px;
}
</style>