<template>
  <mian class="">
    <div class="text-center p-4 dark:bg-slate-800">
      <label for="gold" class="Radio box-border" :class="{ 'active': market === 'gold' }">
        <input type="radio" name="markets" id="gold" checked
        v-model="market" value="gold" class="hidden">금 시세
      </label>
      <label for="oil" class="Radio box-border" :class="{ 'active': market === 'oil' }">
        <input type="radio" name="markets" id="oil"
        v-model="market" value="oil" class="hidden">석유 시세
      </label>
    </div>
    <div v-if="market==='gold'" class="dark:bg-slate-800">
      <GoldPriceView/>
    </div>
    <div v-if="market==='oil'" class="dark:bg-slate-800">
      <OilPriceView/>
    </div>
  </mian>
</template>

<script setup lang="ts">
import GoldPriceView from '@/components/Market/GoldPrice.vue';
import OilPriceView from '@/components/Market/OilPrice.vue';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const marketId = ref(route.params.marketId);
const market = ref(marketId.value)
</script>

<style scoped>
.Radio{
  @apply cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-blue-600 hover:bg-blue-700
}
</style>