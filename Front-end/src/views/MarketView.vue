<template>
  <mian>
    <div class="text-center mt-3">
      <label for="gold" class="Radio" :class="{ 'active': market === 'gold' }">
        <input type="radio" name="markets" id="gold" checked
        v-model="market" value="gold" class="hidden">금 시세
      </label>
      <label for="oil" class="Radio" :class="{ 'active': market === 'oil' }">
        <input type="radio" name="markets" id="oil"
        v-model="market" value="oil" class="hidden">석유 시세
      </label>
    </div>
    <div v-if="market==='gold'">
      <GoldPriceView/>
    </div>
    <div v-if="market==='oil'">
      <OilPriceView/>
    </div>
  </mian>
</template>

<script setup lang="ts">
import GoldPriceView from './Market/GoldPriceView.vue';
import OilPriceView from './Market/OilPriceView.vue';
import { ref } from 'vue';

const market = ref('gold')
</script>

<style scoped>
.Radio{
  @apply cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-blue-600 hover:bg-blue-700
}
</style>