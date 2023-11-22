<template>
  <div class="w-[65%] mx-auto my-8">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <!-- 스피너 -->
      <div class="animate-spin inline-block w-16 h-16 border-[5px] border-current border-t-transparent text-indigo-600 rounded-full dark:text-blue-500 mr-4"></div>
      <span class="text-lg font-semibold text-gray-600 dark:text-gray-300">
        데이터 로드 중...
      </span>
    </div>
    <div v-else class="flex justify-start space-x-4 mt-4">
      <div class="text-2xl">KOSDAQ 지수</div>
      <div class="relative">
        <button @click="showDropdown = !showDropdown" 
          class="flex items-center bg-gradient-to-br from-purple-600 to-blue-500 text-white px-4 py-2 rounded">
          {{ selectedCategory }}
          <svg :class="{ 'rotate-180': showDropdown }" class="w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-if="showDropdown"
          class="absolute mt-2 py-1 w-48 bg-white border border-gray-200 rounded shadow-xl overflow-auto max-h-60">
          <a v-for="category in categories" :key="category" @click="selectCategory(category)"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-400 hover:text-white">
            {{ category }}
          </a>
        </div>
      </div>
    </div>
    <div class="flex justify-start space-x-4 mt-4">
      <button v-for="period in periods" :key="period.value" @click="applyZoom(period.value)"
        :class="{ 'bg-gradient-to-br from-purple-600 to-blue-500 font-extrabold': selectedPeriod === period.value, 'bg-indigo-400': selectedPeriod !== period.value }"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        {{ period.label }}
      </button>
    </div>
    <canvas id="kosdaqChart"></canvas>
  </div>
</template>
  
<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { getKosdaqData } from '@/api/Stock/kosdaq';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
import { subDays, subMonths, subYears, format } from 'date-fns';
import type { KosdaqData } from '@/api/Stock/kosdaq';

Chart.register(...registerables);
Chart.register(zoomPlugin);

const chartRef = ref<Chart>;
const KosdaqData = ref<KosdaqData[]>([]);

const selectedCategory = ref('코스닥')
const selectedPeriod = ref('1M');
const showDropdown = ref(false);
const isLoading = ref(true);

const categories = ['코스닥', '코스닥 150', '코스닥 150 산업재', '코스닥 150 소재', '코스닥 150 자유소비재', '코스닥 150 정보기술', '코스닥 150 커뮤니케이션서비스', '코스닥 150 필수소비재', '코스닥 150 헬스케어', '코스닥 IT', '코스닥 글로벌', '코스닥 기술성장기업부', '코스닥 대형주', '코스닥 벤처기업부', '코스닥 소형주', '코스닥 우량기업부', '코스닥 중견기업부', '코스닥 중형주', 'IT H/W', 'IT S/W & SVC', 'IT부품', '건설', '금속', '금융', '기계·장비', '기타서비스', '기타제조', '디지털컨텐츠', '반도체', '방송서비스', '비금속', '섬유·의류', '소프트웨어', '오락·문화', '운송', '운송장비·부품', '유통', '음식료·담배', '의료·정밀기기', '인터넷', '일반전기전자', '정보기기', '제약', '제조업', '종이·목재', '출판·매체복제', '컴퓨터서비스', '통신방송서비스', '통신서비스', '통신장비'];

const periods = reactive([
  { label: '1주일', value: '1W' },
  { label: '1개월', value: '1M' },
  { label: '3개월', value: '3M' },
  { label: '1년', value: '1Y' },
  { label: '전체', value: 'ALL' }
]);

function selectCategory(category) {
  selectedCategory.value = category;
  showDropdown.value = false;
  applyCategory(category);
};

const applyCategory = (Category) => {
  selectedCategory.value = Category
  const filteredData = KosdaqData.value.filter(data => data.idxNm === Category);
  updateChart(filteredData);
};

const applyZoom = (periodValue) => {
  selectedPeriod.value = periodValue;
  const filteredData = KosdaqData.value.filter(data => data.idxNm === selectedCategory.value);
  const endDate = new Date(filteredData[0].basDt);
  let startDate;

  switch (periodValue) {
    case '1W':
      startDate = subDays(endDate, 9);
      break;
    case '1M':
      startDate = subMonths(endDate, 1);
      break;
    case '3M':
      startDate = subMonths(endDate, 3);
      break;
    case '1Y':
      startDate = subYears(endDate, 1);
      break;
    case 'ALL':
      startDate = new Date(KosdaqData.value[KosdaqData.value.length - 1].basDt); // 가장 오래된 데이터 날짜
      break;
    default:
      startDate = subDays(endDate, 1);
      break;
  }

  if (chartRef.value) {
    chartRef.value.options.scales.x.min = format(startDate, 'yyyy-MM-dd');
    chartRef.value.options.scales.x.max = format(endDate, 'yyyy-MM-dd');
    chartRef.value.update();
  }
};

const updateChart = (filteredData) => {
  if (chartRef.value) {
    chartRef.value.data.labels = filteredData.map(data => data.basDt);
    chartRef.value.data.datasets[0].data = filteredData.map(data => data.clpr);
    chartRef.value.data.datasets[0].label = selectedCategory.value;
    applyZoom('1M'); // 변경할 때 기본적으로 1개월
    chartRef.value.update();
  }
};

onMounted(async () => {
  const ctx = document.getElementById('kosdaqChart') as HTMLCanvasElement;

  if (ctx) {
    try {
      KosdaqData.value = await getKosdaqData();

      const chartData = {
        labels: KosdaqData.value.map(data => data.basDt),
        datasets: [{
          label: selectedCategory.value,
          data: KosdaqData.value.map(data => data.clpr),
          fill: true,
          backgroundColor: 'rgba(167, 139, 250, 0.2)',
          borderColor: 'rgba(167, 139, 250, 1)',
          tension: 0.1
        }]
      };

      chartRef.value = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          hoverRadius: 18,
          hoverBackgroundColor: 'rgba(167, 139, 250, 1)',
          responsive: true,
          interaction: {
          intersect: false,
          },
          scales: {
            y: {
              ticks: {
                font: {
                  size: 18,
                  weight: 'bold'
                }
              },
              beginAtZero: false,
              grace: '5%'
            },
            x: {
              type: 'time',
              time: {
                unit: 'day',
                tooltipFormat: 'PPP',
                displayFormats: {
                  day: 'PP'
                }
              },
            }
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              enabled: true,
              mode: 'index',
              intersect: false,
              bodyFont: {
                size: 20
              }, // 본문 폰트 사이즈
              titleFont: {
                size: 14
              }, // 제목 폰트 사이즈
            },
            zoom: {
              zoom: {
                wheel: {
                  enabled: true,
                },
                pinch: {
                  enabled: true
                },
                mode: 'x',
              },
              pan: {
                enabled: true,
                mode: 'x',
              },
              limits: {
                x: { min: 'original', max: 'original', minRange: 1 },
              }
            }
          }
        }
      });

      // 기본적으로 코스닥 표시
      applyCategory(selectedCategory.value);
    } catch (error) {
      console.error('There was an error fetching the kosdaq data: ', error);
    } finally {
      isLoading.value = false; // 로딩 완료
    }
  }
});
</script>
