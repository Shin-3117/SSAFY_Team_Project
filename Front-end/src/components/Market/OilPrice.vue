<template>
  <div class="w-[75%] mx-auto my-8">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <!-- 스피너 -->
      <div class="animate-spin inline-block w-16 h-16 border-[5px] border-current border-t-transparent text-green-600 rounded-full dark:text-green-500 mr-4"></div>
      <span class="text-lg font-semibold text-gray-600 dark:text-gray-300">
        데이터 로드 중...
      </span>
    </div>
    <div v-else class="flex justify-start space-x-4 mt-4">
      <div class="text-2xl">유가 시세</div>
      <button v-for="category in categories" :key="category"    @click="applyCategory(category)"
        :class="{'bg-green-600 font-extrabold': selectedCategory === category, 'bg-green-500': selectedCategory !== category}"
        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
        {{ category }}
      </button>
    </div>
    <div class="flex justify-start space-x-4 mt-4">
      <button v-for="period in periods" :key="period.value" @click="applyZoom(period.value)"
        :class="{'bg-green-600 font-extrabold': selectedPeriod === period.value, 'bg-green-500': selectedPeriod !== period.value}"
        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
        {{ period.label }}
      </button>
    </div>
    <canvas id="oilChart"></canvas>
  </div>
</template>
  
<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { getOilData } from '@/api/Market/oil.js';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
import { subDays, subMonths, subYears, format } from 'date-fns';
import type { OilData } from '@/api/Market/oil.js';

Chart.register(...registerables);
Chart.register(zoomPlugin);

const chartRef = ref<Chart>;
const oilData = ref<OilData[]>([]);

const selectedCategory = ref('휘발유')
const selectedPeriod = ref('1M');
const isLoading = ref(true);

const categories = ['휘발유', '경유', '등유'];

const periods = reactive([
  { label: '1주일', value: '1W' },
  { label: '1개월', value: '1M' },
  { label: '3개월', value: '3M' },
  { label: '1년', value: '1Y' },
  { label: '전체', value: 'ALL' }
]);

const applyCategory = (Category) => {
  selectedCategory.value = Category
  const filteredData = oilData.value.filter(data => data.oilCtg === Category);
  updateChart(filteredData);
};

const applyZoom = (periodValue) => {
  selectedPeriod.value = periodValue;
  const filteredData = oilData.value.filter(data => data.oilCtg === selectedCategory.value);
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
      startDate = new Date(oilData.value[oilData.value.length - 1].basDt); // 가장 오래된 데이터 날짜
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
    chartRef.value.data.datasets[0].data = filteredData.map(data => data.wtAvgPrcDisc);
    chartRef.value.data.datasets[0].label = `${selectedCategory.value} 시세(원/L)`;
    applyZoom('1M'); // 유종을 변경할 때 기본적으로 1개월
    chartRef.value.update();
  }
};

onMounted(async () => {
  const ctx = document.getElementById('oilChart') as HTMLCanvasElement;

  if (ctx) {
    try {
      oilData.value = await getOilData();

      const chartData = {
        labels: oilData.value.map(data => data.basDt),
        datasets: [{
          label: `${selectedCategory.value} 시세(원/L)`,
          data: oilData.value.map(data => data.wtAvgPrcDisc),
          fill: true,
          backgroundColor: 'rgba(0,128,0, 0.2)',
          borderColor: 'green',
          tension: 0.1
        }]
      };

      chartRef.value = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          hoverRadius: 18,
          hoverBackgroundColor: 'green',
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

      // 기본적으로 첫 번째 유종을 표시
      applyCategory(selectedCategory.value);
    } catch (error) {
      console.error('There was an error fetching the oil data: ', error);
    } finally {
      isLoading.value = false; // 로딩 완료
    }
  }
});
</script>
@/api/Market/oil@/api/Market/oil