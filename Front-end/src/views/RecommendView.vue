<template>
  <div class="container mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-4">투자 추천</h1>

    <!-- 사용자 입력 UI -->
    <div class="flex items-center mb-4">
      <input v-model="days" type="number" placeholder="일 수 입력 (예: 90)"
        class="mr-2 p-2 border border-gray-300 rounded focus:outline-none focus:border-indigo-500">
      <button @click="loadData" class="p-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 focus:outline-none">
        데이터 로드
      </button>
    </div>

    <div v-if="loading" class="flex justify-center items-center h-screen">
      <!-- 스피너 -->
      <div
        class="animate-spin inline-block w-16 h-16 border-[5px] border-current border-t-transparent text-indigo-600 rounded-full dark:text-blue-500 mr-4">
      </div>
      <span class="text-lg font-semibold text-gray-600 dark:text-gray-300">
        데이터 로드 중...
      </span>
    </div>

    <div v-else class="flex flex-wrap">
      <!-- 카테고리 선택 버튼 -->
      <div class="mb-4">
        <button v-for="category in categories" :key="category"
          :class="{ 'bg-gradient-to-br from-purple-600 to-blue-500 font-extrabold': selectedCategory === category }"
          class="mr-2 mb-2 p-2 bg-indigo-400 text-white rounded hover:bg-gradient-to-br from-purple-600 to-blue-500 focus:outline-none animate-jump-in animate-once animate-duration-[1100ms]"
          @click="selectedCategory = category">
          {{ category }}
        </button>
      </div>
      <div v-if="investmentData[selectedCategory]" class="p-4 border border-gray-200 rounded shadow w-full lg:w-3/4 bg-gradient-to-br from-blue-300 to-red-300">
        <h2 class="text-2xl font-bold mb-2">{{ selectedCategory }} 투자 지표</h2>

        <div class="flex justify-between">
          <div class="w-1/2 pr-2 bg-blue-200">
            <h3 class="text-lg ml-2 font-semibold mb-2">Plus(상승%)</h3>
            <ul>
              <li v-for="item in positiveItems" :key="item.Name" class="my-2 animate-fade-up animate-duration-[1500ms] ml-2">
                <span class="font-medium">{{ item.Name }}</span>: <span class="font-bold text-blue-600">{{ item.Indicator }}%</span>
              </li>
            </ul>
          </div>

          <div class="w-1/2 pl-2 bg-red-200">
            <h3 class="text-lg font-semibold mb-2">Minus(하락%)</h3>
            <ul>
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
    const days = ref();  // 기본값 설정
    const selectedCategory = ref<string | null>(null);
    const categories = ref<string[]>([]);

    const loadData = () => {
      loading.value = true;
      axios.get(`${baseURL}/market/recommend_data/${days.value}/`)
        .then(response => {
          investmentData.value = response.data;
          categories.value = ['Gold', 'Oil', 'Kospi', 'Kosdaq', 'KRX', 'Theme'];
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
        ? investmentData.value[selectedCategory.value].filter(item => item.Indicator < 0)
        : [];
    });

    return {
      investmentData,
      loading,
      days,
      selectedCategory,
      categories,
      loadData,
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