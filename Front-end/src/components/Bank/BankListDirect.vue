<template>
  <section>
    <ul v-for="deposit in depositList">
      <li>
        <div class="flex">
          <p class="px-3">{{ deposit.kor_co_nm }}</p>
          <p>{{ deposit.fin_prdt_nm }}</p>
        </div>
        <div>
          <p>가입방법: {{ deposit.join_way }}</p>
        </div>
        <ul v-for="option in deposit.options">
          <li>
            <span>{{ option.intr_rate_type_nm }} | </span>
            <span>기간:{{ option.save_trm }} | </span>
            <span>금리:{{ option.intr_rate }} | </span>
            <span>우대금리:{{ option.intr_rate2 }}</span>
          </li>
        </ul>
      </li>
      <hr>
    </ul>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import getDepositListDirect from '../../api/bankDirect';
// const apiKey = import.meta.env.VITE_API_KEY
// const apiUrl = import.meta.env.VITE_API_URL

const depositList = ref('데이터 로딩중 입니다');
onMounted(async () => {
  try {
    const response = await getDepositListDirect();
    for (const bank of response.result.baseList){
      bank.options = []
      for(const option of response.result.optionList){
        if(bank.fin_prdt_cd === option.fin_prdt_cd){
          bank.options.push(option)
        }
      }
    }
    depositList.value = response.result.baseList;
  } catch (error) {
    console.error(error);
  }
});

</script>




<style scoped>

</style>