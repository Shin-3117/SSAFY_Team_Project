<template>
  <button @click="toggleDark()"
  class="btn">
    {{ isDark ? "Dark" : "Light" }} Mode
  </button>
</template>

<script setup lang="ts">
// 다크모드 적용
import { useDark, useToggle } from "@vueuse/core";
const isDark = useDark();
const toggleDark = useToggle(isDark)
</script>

<style scoped>
.btn {
  @apply font-bold py-2 px-4 rounded-full
  bg-slate-500 text-white 
  dark:text-black;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>