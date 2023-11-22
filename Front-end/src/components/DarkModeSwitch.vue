<template>
  <button @click="toggleDark()"
  class="btn animate-rotate-y">
    <!-- {{ isDark ? "Dark" : "Light" }} Mode -->
    <img src="@/assets/sun-solid.svg" alt="Light Mode" v-if="!isDark" class="modeImg animate-rotate-y">
    <img src="@/assets/moon-solid.svg" alt="Dark Mode" v-if="isDark" class="modeImg animate-rotate-y">
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
  @apply font-bold p-2 rounded-full
  bg-slate-500 text-white 
  dark:text-black;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
.modeImg{
  width: 24px;
  height: 24px;
}
</style>