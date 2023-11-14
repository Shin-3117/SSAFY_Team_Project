<template>
  <section>
    <div>
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
        <label for="term6">
          <input type="radio" name="term" id="term6" checked
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
        <p>{{ radioValue }}</p>
      </div>

      <button @click="changeData">조회</button>
    </div>

    <table class="table-auto">
      <thead class="bg-yellow-300 dark:bg-yellow-700">
        <tr>
          <th>상품명</th>
          <th>금리</th>
          <th>기간</th>
          <th>은행</th>
        </tr>
      </thead>
      <tbody v-if="depositList">
        <tr v-for="deposit in depositList" class="bg-green-100 dark:bg-green-900">
          <td class="p-2">{{deposit.fin_prdt_cd.fin_prdt_nm}}</td>
          <td class="p-2">{{deposit.intr_rate}}</td>
          <td class="p-2">{{deposit.save_trm}}</td>
          <td class="p-2">{{deposit.fin_prdt_cd.kor_co_nm}}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import getBankList from '../../api/bankDeposit';

const radioValue = ref({
  Saving: 'deposit',
  term:'6',
  sort_field: 'intr_rate'
})

const depositList = ref(false);

onMounted(async () => {
  try {
    const response = await getBankList();
    depositList.value = response;
  } catch (error) {
    console.error(error);
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

</style>