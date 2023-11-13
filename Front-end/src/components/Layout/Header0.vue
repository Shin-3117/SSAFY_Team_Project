<template>
  <header>
    <h1>프로젝트이름</h1>
    <nav>
      <RouterLink to="/">예금 적금</RouterLink>
      |
      <RouterLink to="/ExchangeRate">환율</RouterLink>
      |
      <RouterLink to="/map">내 주위 은행 찾기</RouterLink>
      |
      <RouterLink to="/recommend">추천</RouterLink>
    </nav>
    <AuthBtn/>
  </header>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AuthBtn from '../Auth/AuthBtn.vue';
</script>

<style scoped>
header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background-color: antiquewhite;
}
</style>