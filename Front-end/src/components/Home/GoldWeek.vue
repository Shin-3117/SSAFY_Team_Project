<template>
  <div class="w-80 mx-auto my-8 border-4 rounded-xl p-2 border-yellow-200 h-56">
    <div class="flex justify-between items-center mb-4 ml-1">
      <span class="text-xl font-semibold animate-rotate-x animate-twice animate-duration-[1200ms]">
        금 시세 <span class="text-2xl text-yellow-500 font-semibold">{{ gold_cur }}<span class="text-xl">원/g</span></span>
      </span>
      <!-- SVG 아이콘 -->
      <div class="relative group">
        <router-link to="/Market/gold">
            <div
              class="border-solid border-2 rounded-lg border-yellow-300 text-black mr-1 animate-rotate-y animate-twice animate-duration-[1200ms] bg-yellow-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
              </svg>
            </div>
        </router-link>
        <div
          class="opacity-0 invisible group-hover:opacity-100 group-hover:visible absolute w-28 mt-2  text-gray-800 shadow-lg transition duration-300 ease-in-out transform group-hover:animate-fade-down border-solid border-2 rounded-lg border-yellow-300 bg-yellow-100">
          <p class="px-4 py-2 text-sm text-center font-semibold text-gray-600 hover:text-gray-800">
            차트로 이동
          </p>
        </div>
      </div>
    </div>
    <!-- 차트 캔버스 -->
    <div>
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import axios from 'axios';
import config from '../../config';

const baseURL = config.baseURL;
const canvas = ref<HTMLCanvasElement>();

interface GoldData {
  id: number;
  basDt: string;
  itmsNm: string;
  clpr: string;
}

let myChart: Chart | null = null;
const gold_cur = ref();

onMounted(async () => {
  const ctx = canvas.value?.getContext('2d');
  if (!ctx) return;

  try {
    const response = await axios.get<GoldData[]>(`${baseURL}/market/send_main/gold/`);
    gold_cur.value = parseFloat(response.data[0].clpr)
    const data = {
      labels: response.data.map((data) => data.basDt),
      datasets: [
        {
          label: 'GOLD',
          fill: true,
          backgroundColor: 'rgba(212, 175, 55, 0.5)',
          borderColor: 'rgba(212, 175, 55, 1)',
          data: response.data.map((data) => parseFloat(data.clpr)),
          tension: 0.2
        },
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
  } catch (error) {
    console.error('Failed to fetch GOLD data:', error);
  }
});

</script>


<style scoped>
.card {
  @apply rounded-xl border-4 p-2;
}
</style>