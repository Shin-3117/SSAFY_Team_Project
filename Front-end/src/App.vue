<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/Layout/Header.vue';
import Footer from './components/Layout/Footer.vue';
</script>

<template>
  <Header/>

  <RouterView class="bg-white  dark:bg-slate-800 dark:text-slate-200"/>

  <Footer/>
</template>

<style scoped>

</style>
