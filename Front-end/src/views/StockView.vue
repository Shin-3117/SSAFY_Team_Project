<template>
<main>
  <div class="text-center p-4 dark:bg-slate-800 flex justify-center gap-4">
    <label for="Kospi" class="Radio box-border" :class="{ 'active': Stock === 'Kospi' }">
      <input type="radio" name="Stocks" id="Kospi" checked
      v-model="Stock" value="Kospi" class="hidden">KOSPI
    </label>
    <label for="Kosdaq" class="Radio box-border" :class="{ 'active': Stock === 'Kosdaq' }">
      <input type="radio" name="Stocks" id="Kosdaq"
      v-model="Stock" value="Kosdaq" class="hidden">KOSDAQ
    </label>
    <label for="Krx" class="Radio box-border" :class="{ 'active': Stock === 'Krx' }">
      <input type="radio" name="Stocks" id="Krx"
      v-model="Stock" value="Krx" class="hidden">KRX
    </label>
    <label for="Theme" class="Radio box-border" :class="{ 'active': Stock === 'Theme' }">
      <input type="radio" name="Stocks" id="Theme"
      v-model="Stock" value="Theme" class="hidden">테마
    </label>
  </div>
  <div v-if="Stock==='Kospi'" class="dark:bg-slate-800">
    <Kospi/>
  </div>
  <div v-if="Stock==='Kosdaq'" class="dark:bg-slate-800">
    <Kosdaq/>
  </div>
  <div v-if="Stock==='Krx'" class="dark:bg-slate-800">
    <Krx/>
  </div>
  <div v-if="Stock==='Theme'" class="dark:bg-slate-800">
    <Theme/>
  </div>
</main>
</template>

<script setup lang="ts">
import Kospi from '@/components/Stock/Kospi.vue';
import Kosdaq from '@/components/Stock/Kosdaq.vue';
import Krx from '@/components/Stock/Krx.vue';
import Theme from '@/components/Stock/Theme.vue';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const stockId = ref(route.params.stockId);
const Stock = ref(stockId.value)
</script>

<style scoped>
.Radio{
  @apply cursor-pointer bg-indigo-400 hover:bg-gradient-to-br from-purple-600 to-blue-500 text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-blue-700;
  transform: scale(1.2);
}
</style>