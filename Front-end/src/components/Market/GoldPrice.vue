<template>
  <div class="w-[65%] mx-auto my-8">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <!-- 스피너 -->
      <div
        class="animate-spin inline-block w-16 h-16 border-[5px] border-current border-t-transparent text-yellow-400 rounded-full dark:text-blue-500 mr-4">
      </div>
      <span class="text-lg font-semibold text-gray-600 dark:text-gray-300">
        데이터 로드 중...
      </span>
    </div>
    <div v-else>
      <div class="text-2xl">국내 금 시세</div>
      <div class="flex justify-start space-x-4 mt-4">
        <button v-for="period in periods" :key="period.value" @click="applyZoom(period.value)"
          :class="{ 'bg-yellow-500 font-extrabold': selectedPeriod === period.value, 'bg-yellow-600': selectedPeriod !== period.value }"
          class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-400">
          {{ period.label }}
        </button>
      </div>
    </div>
    <canvas id="goldChart"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { getGoldData } from '@/api/Market/gold.js';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
import { subDays, subMonths, subYears, format } from 'date-fns';
import type { GoldData } from '@/api/Market/gold.js';

Chart.register(...registerables);
Chart.register(zoomPlugin);

const chartRef = ref<Chart>;
const goldData = ref<GoldData[]>([]);

const selectedPeriod = ref('1M');
const isLoading = ref(true);

const periods = reactive([
  { label: '1주일', value: '1W' },
  { label: '1개월', value: '1M' },
  { label: '3개월', value: '3M' },
  { label: '1년', value: '1Y' },
  { label: '전체', value: 'ALL' }
]);

const applyZoom = (periodValue) => {
  selectedPeriod.value = periodValue;
  const endDate = new Date(goldData.value[0].basDt);
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
      startDate = new Date(goldData.value[goldData.value.length - 1].basDt); // 가장 오래된 데이터 날짜
      break;
    default:
      startDate = subDays(endDate, 1);
      break;
  }

  if (chartRef.value) {
    chartRef.value.options.scales.x.min = format(startDate, 'yyyy-MM-dd');
    chartRef.value.options.scales.x.max = format(endDate, 'yyyy-MM-dd');
    chartRef.value.update(); // 변경된 옵션을 차트에 적용
  }
};

onMounted(async () => {
  const ctx = document.getElementById('goldChart') as HTMLCanvasElement;

  if (ctx) {
    try {
      goldData.value = await getGoldData();

      const chartData = {
        labels: goldData.value.map(data => data.basDt),
        datasets: [{
          label: '국내 금 시세(원/g)',
          data: goldData.value.map(data => data.clpr),
          fill: true,
          backgroundColor: 'rgba(255, 223, 0, 0.2)',
          borderColor: 'gold',
          tension: 0.1
        }]
      };

      chartRef.value = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          hoverRadius: 18,
          hoverBackgroundColor: 'gold',
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

      applyZoom('1M'); // 기본적으로 1개월 표시
    } catch (error) {
      console.error('There was an error fetching the gold data: ', error);
    } finally {
      isLoading.value = false; // 로딩 완료
    }
  }
});
</script>
@/api/Market/gold@/api/Market/gold