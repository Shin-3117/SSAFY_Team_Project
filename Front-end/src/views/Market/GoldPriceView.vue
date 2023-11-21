<template>
  <div class="w-[75%] mx-auto my-8">
    <div class="text-2xl">국내 금 시세</div>
    <div class="flex justify-start space-x-4 mt-4">
      <button v-for="period in periods" :key="period.value" @click="applyZoom(period.value)"
        :class="{'bg-yellow-500 font-extrabold': selectedPeriod === period.value, 'bg-blue-500': selectedPeriod !== period.value}"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        {{ period.label }}
      </button>
    </div>
    <canvas id="goldChart"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { getGoldData } from '@/api/gold';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
import { subDays, subMonths, subYears, format } from 'date-fns';
import type { GoldData } from '@/api/gold';

Chart.register(...registerables);
Chart.register(zoomPlugin);

const chartRef = ref<Chart>;
const goldData = ref<GoldData[]>([]);

const selectedPeriod = ref('1M');

const periods = reactive([
  { label: '전체', value: 'ALL' },
  { label: '1년', value: '1Y' },
  { label: '3개월', value: '3M' },
  { label: '1개월', value: '1M' },
  { label: '1주일', value: '1W' }
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
          label: '국내 금 시세(매매기준율 ￦/g)',
          data: goldData.value.map(data => data.clpr),
          fill: false,
          borderColor: 'gold',
          tension: 0.1
        }]
      };

      chartRef.value = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          scales: {
            y: {
              beginAtZero: false,
              grace: '5%'
            },
            x: {
              type: 'time',
              time: {
                unit: 'day'
              },
            }
          },
          plugins: {
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
    }
  }
});
</script>
