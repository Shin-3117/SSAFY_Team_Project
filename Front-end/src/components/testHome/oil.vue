<template>
  <div :class="`w-80 mx-auto my-8 border-4 rounded-xl p-2 border-${currentColor}`">
    <div class="flex justify-between items-center mb-4 ml-1">
      <span class="text-xl font-semibold animate-rotate-x animate-twice animate-duration-[1200ms]">
        <span :class="`text-2xl font-semibold text-${currentColor}`">{{ currentOil }} {{ latestPrice }}</span>
      </span>
      <div class="relative group">
        <router-link to="/Market/oil">
          <div :class="`border-solid border-2 rounded-lg border-${currentColor} mr-1 animate-rotate-y animate-twice animate-duration-[1200ms] bg-${currentColor}`">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
            </svg>
          </div>
        </router-link>
        <div :class="`opacity-0 invisible group-hover:opacity-100 group-hover:visible absolute w-28 mt-2 text-gray-800 shadow-lg transition duration-300 ease-in-out transform group-hover:animate-fade-down border-solid border-2 rounded-lg border-${currentColor} bg-white`">
          <p class="px-4 py-2 text-sm text-center font-semibold text-gray-600 hover:text-gray-800">
            차트로 이동
          </p>
        </div>
      </div>
    </div>
    <div>
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import axios from 'axios';
import config from '../../config';

const baseURL = config.baseURL;
const canvas = ref<HTMLCanvasElement>();
const latestPrice = ref('');
const currentColor = ref('');
const currentOil = ref('');

function classifyOilData(data) {
  const oilData = { 경유: [], 등유: [], 휘발유: [] };
  data.forEach(item => {
    oilData[item.oilCtg].push({ date: item.basDt, price: item.wtAvgPrcDisc });
  });
  return oilData;
}

const oilData = ref({ 경유: [], 등유: [], 휘발유: [] });
let myChart = null;
let currentOilIndex = 0;
const oilTypes = ['경유', '등유', '휘발유'];
const oilColors = {
  경유: '[#FF6384]',
  등유: '[#36A2EB]',
  휘발유: '[#4BC0C0]',
};

onMounted(async () => {
  const ctx = canvas.value?.getContext('2d');
  if (!ctx) return;

  try {
    const response = await axios.get(`${baseURL}/market/send_main/oil/`);
    const classifiedData = classifyOilData(response.data);
    oilData.value = classifiedData;
    updateLatestPriceAndColor();

    const data = {
      labels: classifiedData['경유'].map(item => item.date),
      datasets: [
        // 각 유종에 대한 데이터셋 생성
        {
          label: '경유',
          data: classifiedData['경유'].map(item => parseFloat(item.price)),
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.4)',
          fill: true,
        },
        {
          label: '등유',
          data: classifiedData['등유'].map(item => parseFloat(item.price)),
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.4)',
          fill: true,
        },
        {
          label: '휘발유',
          data: classifiedData['휘발유'].map(item => parseFloat(item.price)),
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.4)',
          fill: true,
        }
      ],
    };

    const options = {
      interaction: {
        intersect: false,
      },
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          ticks: {
            maxTicksLimit: 5,
            font: {
              size: 15,
              weight: 'bold'
            }
          },
          beginAtZero: false,
          grace: '20%'
        },
        x: {
          ticks: {
            display: false
          },
          type: 'time',
          time: {
            unit: 'day',
            tooltipFormat: 'PPP',
            displayFormats: {
              day: 'dd'
            }
          },
        }
      }
    };

    myChart = new Chart(ctx, {
      type: 'line',
      data: data,
      options: options,
    });

    const intervalId = setInterval(() => {
      currentOilIndex = (currentOilIndex + 1) % oilTypes.length;
      updateLatestPriceAndColor();
    }, 1500);

    onUnmounted(() => {
      clearInterval(intervalId);
    });
  } catch (error) {
    console.error('Failed to fetch OIL data:', error);
  }
});

function updateLatestPriceAndColor() {
  const currentOilType = oilTypes[currentOilIndex];
  currentOil.value = currentOilType;
  const currentOilData = oilData.value[currentOilType];
  if (currentOilData && currentOilData.length > 0) {
    latestPrice.value = currentOilData[0].price + '원/L';
    currentColor.value = oilColors[currentOilType];
  }
}
</script>
