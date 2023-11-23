<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/Layout/Header.vue';
import Footer from './components/Layout/Footer.vue';
</script>

<template>
  <Header/>

  <RouterView class="view bg-white  dark:bg-slate-800 dark:text-slate-200"/>

  <Footer/>
</template>

<style>
input{
  @apply border border-slate-500 dark:bg-slate-900 mb-4 rounded-xl px-2
}
.view{
  min-height: calc(100vh - 88px);
}
</style>
