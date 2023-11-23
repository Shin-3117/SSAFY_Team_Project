<template>
  <main class="view">
    <div class="text-center p-4 dark:bg-slate-800 flex justify-center gap-4">
      <label for="gold" class="Radio box-border bg-yellow-600 hover:bg-yellow-500" :class="{ 'active': market === 'gold' }">
        <input type="radio" name="markets" id="gold" checked
        v-model="market" value="gold" class="hidden">금 시세
      </label>
      <label for="oil" class="Radio box-border bg-green-600 hover:bg-green-500" :class="{ 'active2': market === 'oil' }">
        <input type="radio" name="markets" id="oil"
        v-model="market" value="oil" class="hidden">석유 시세
      </label>
    </div>
    <div v-if="market==='gold'" class="dark:bg-slate-800">
      <GoldPrice/>
    </div>
    <div v-if="market==='oil'" class="dark:bg-slate-800">
      <OilPrice/>
    </div>
  </main>
</template>

<script setup lang="ts">
import GoldPrice from '@/components/Market/GoldPrice.vue';
import OilPrice from '@/components/Market/OilPrice.vue';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const marketId = ref(route.params.marketId);
const market = ref(marketId.value)
</script>

<style scoped>
.Radio{
  @apply cursor-pointer text-white font-bold py-2 px-4 rounded;
}
.Radio.active {
  @apply bg-yellow-500 hover:bg-yellow-400;
  transform: scale(1.2);
}
.Radio.active2 {
  @apply bg-green-500 hover:bg-green-400;
  transform: scale(1.2);
}
</style>