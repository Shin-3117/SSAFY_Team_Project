<template>
  <div class="w-[75%] mx-auto my-8">
    <div class="flex justify-start space-x-4 mt-4">
      <div class="text-2xl">유가 시세</div>
      <button v-for="category in categories" :key="category"    @click="applyCategory(category)"
        :class="{'bg-green-500 font-extrabold': selectedCategory === category, 'bg-blue-500': selectedCategory !== category}"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        {{ category }}
      </button>
    </div>
    <div class="flex justify-start space-x-4 mt-4">
      <button v-for="period in periods" :key="period.value" @click="applyZoom(period.value)"
        :class="{'bg-green-500 font-extrabold': selectedPeriod === period.value, 'bg-blue-500': selectedPeriod !== period.value}"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        {{ period.label }}
      </button>
    </div>
    <canvas id="oilChart"></canvas>
  </div>
</template>
  
<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { getOilData } from '@/api/oil';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
import { subDays, subMonths, subYears, format } from 'date-fns';
import type { OilData } from '@/api/oil';

Chart.register(...registerables);
Chart.register(zoomPlugin);

const chartRef = ref<Chart>;
const oilData = ref<OilData[]>([]);

const selectedCategory = ref('경유')
const selectedPeriod = ref('1M');

const categories = ['경유', '등유', '휘발유'];

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
          label: '유가 시세(￦/L)',
          data: oilData.value.map(data => data.wtAvgPrcDisc),
          fill: false,
          borderColor: 'green',
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

      // 기본적으로 첫 번째 유종을 표시
      applyCategory(selectedCategory.value);
    } catch (error) {
      console.error('There was an error fetching the oil data: ', error);
    }
  }
});
</script>
