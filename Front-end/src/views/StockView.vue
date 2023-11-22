<template>
<mian class="">
  <div class="text-center p-4 dark:bg-slate-800">
    <label for="Kospi" class="Radio box-border" :class="{ 'active': Stock === 'Kospi' }">
      <input type="radio" name="Stocks" id="Kospi" checked
      v-model="Stock" value="Kospi" class="hidden">Kospi
    </label>
    <label for="Kosdaq" class="Radio box-border" :class="{ 'active': Stock === 'Kosdaq' }">
      <input type="radio" name="Stocks" id="Kosdaq"
      v-model="Stock" value="Kosdaq" class="hidden">Kosdaq
    </label>
    <label for="Krx" class="Radio box-border" :class="{ 'active': Stock === 'Krx' }">
      <input type="radio" name="Stocks" id="Krx"
      v-model="Stock" value="Krx" class="hidden">Krx
    </label>
    <label for="Theme" class="Radio box-border" :class="{ 'active': Stock === 'Theme' }">
      <input type="radio" name="Stocks" id="Theme"
      v-model="Stock" value="Theme" class="hidden">Theme
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
</mian>
</template>

<script setup lang="ts">
import Kospi from '@/components/Stock/Kospi.vue';
import Kosdaq from '@/components/Stock/Kosdaq.vue';
import Krx from '@/components/Stock/Krx.vue';
import Theme from '@/components/Stock/Theme.vue';
import { ref } from 'vue';

const Stock = ref('Kospi')
</script>

<style scoped>
.Radio{
  @apply cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-blue-600 hover:bg-blue-700
}
</style>