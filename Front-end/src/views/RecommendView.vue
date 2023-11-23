<template>
  <div class="container mx-auto p-6 flex flex-col items-center">
    <h1 class="text-2xl font-semibold mb-4 animate-fade animate-duration-[1800ms]">투자 추천</h1>
    <!-- 사용자 입력 UI -->
    <div class="flex items-center mb-4 animate-fade animate-duration-[1800ms]">
      <input v-model="days" placeholder="현재 날짜로부터 계산할 데이터 수 (1개 = 1일)"
        class="m-2 p-2 border-2 border-gray-300 rounded-md 
        focus:outline-none focus:border-indigo-500 w-96 
        font-semibold text-center">
      <button @click="loadData" class="p-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 focus:outline-none">
        데이터 로드
      </button>
    </div>

    <div v-if="!dataLoaded">
      <div class="animate-fade animate-duration-[1800ms]">
      <p class="temp font-semibold text-violet-500 text-xl leading-loose ml-40"><br>SS INVEST에서는 금과 석유에 대한 시세와<br>주가지수(KOSPI, KOSDAQ, KRX, 테마) 시세에 대한 데이터를<br>2022년부터 현재까지 약 7만개 보유중입니다.<br><br>현재 날짜로부터 역순으로 포함할 데이터의 개수를 입력하시면<br>해당 기간 동안의 모든 데이터를 분석하여 상승 / 하락에 대한 지표를<br>비율(%)로 제공합니다.<br><br>결과를 참고하여 투자에 도움이 되기를 바랍니다.</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center h-auto">
      <!-- 스피너 -->
      <div
        class="animate-spin inline-block w-16 h-16 border-[5px] border-current border-t-transparent text-indigo-600 rounded-full dark:text-blue-500 mr-4">
      </div>
      <span class="text-lg font-semibold text-gray-600 dark:text-gray-300">
        데이터 로드 중...
      </span>
    </div>

    <div v-else class="flex flex-wrap flex-col items-center justify-center">
      <!-- 카테고리 선택 버튼 -->
      <div class="mb-4">
        <button v-for="category in categories" :key="category"
          :class="{ 'bg-gradient-to-br from-purple-600 to-blue-500 font-extrabold': selectedCategory === category }"
          class="mr-2 mb-2 p-2 bg-indigo-400 text-white rounded hover:bg-gradient-to-br from-purple-600 to-blue-500 focus:outline-none animate-jump-in animate-once animate-duration-[1100ms]"
          @click="selectedCategory = category">
          {{ category }}
        </button>
      </div>
      <div v-if="investmentData[selectedCategory]" class="p-4 border border-gray-200 rounded-lg shadow temp bg-gradient-to-br from-blue-300 to-red-300 animate-fade animate-duration-[1500ms]">
        <h2 class="text-2xl font-bold mb-4">{{ selectedCategory }} 투자 지표</h2>
        <div class="flex justify-between">
          <div class="w-1/2 pr-2 bg-blue-200">
            <h3 class="text-lg ml-2 font-semibold mb-2"><span class="text-blue-600">Plus</span>(상승%)</h3>
            <ul class="overflow-auto temp2">
              <li v-for="item in positiveItems" :key="item.Name" class="my-2 animate-fade-up animate-duration-[1500ms] ml-2">
                <span class="font-medium">{{ item.Name }}</span>: <span class="font-bold text-blue-600">{{ item.Indicator }}%</span>
              </li>
            </ul>
          </div>

          <div class="w-1/2 px-2 bg-red-200">
            <h3 class="text-lg font-semibold mb-2"><span class="text-red-600">Minus</span>(하락%)</h3>
            <ul class="overflow-auto temp2">
              <li v-for="item in negativeItems" :key="item.Name" class="my-2 animate-fade-down animate-duration-[1500ms]">
                {{ item.Name }}: <span class="font-bold text-red-600">{{ item.Indicator }}%</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import axios from 'axios';
import config from '@/config';

const baseURL = config.baseURL;

export default defineComponent({
  setup() {
    const investmentData = ref<any>({});
    const loading = ref(false);
    const dataLoaded = ref(false);
    const days = ref();  // 기본값 설정
    const selectedCategory = ref<string | null>(null);
    const categories = ref<string[]>([]);

    const loadData = () => {
      loading.value = true;
      dataLoaded.value = true;
      axios.get(`${baseURL}/market/recommend_data/${days.value}/`)
        .then(response => {
          investmentData.value = response.data;
          categories.value = ['금', '석유', 'KOSPI', 'KOSDAQ', 'KRX', '테마'];
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
          loading.value = false;
        });
    };

    const positiveItems = computed(() => {
      return selectedCategory.value && Array.isArray(investmentData.value[selectedCategory.value])
        ? investmentData.value[selectedCategory.value].filter(item => item.Indicator > 0)
        : [];
    });

    const negativeItems = computed(() => {
      return selectedCategory.value && Array.isArray(investmentData.value[selectedCategory.value])
        ? investmentData.value[selectedCategory.value].filter(item => item.Indicator < 0).sort((a, b) => a.Indicator - b.Indicator)
        : [];
    });

    return {
      investmentData,
      loading,
      days,
      selectedCategory,
      categories,
      loadData,
      dataLoaded,
      positiveItems,
      negativeItems,
      debugData() {
        console.log('Investment Data:', investmentData.value);
        console.log('Positive Items:', positiveItems.value);
        console.log('Negative Items:', negativeItems.value);
      }
    };
  }
});
</script>

<style scoped>
.temp{
  width : 740px;
}

.temp2{
  height: 500px;
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