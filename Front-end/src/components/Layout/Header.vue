<template>
  <header class="bg-slate-800 dark:bg-slate-900 text-white">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex mr-6">
        <RouterLink to="/" class="flex justify-center items-center">
          <h1 class="hidden">SSInvest</h1>
          <img src="../../assets/img/Logo/LogoImg.png" alt="Logo" class="h-10">
          <img src="../../assets/img/Logo/LogoWord.png" alt="Logo" class="h-6 lg:hidden xl:block ml-2">
        </RouterLink>
      </div>
      <div class="flex lg:hidden">
        <button type="button" class="p-2 inline-flex items-center justify-center text-gray-500" @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>
      <PopoverGroup class="hidden lg:flex lg:gap-x-12">
        <RouterLink to="/bank" class="navLink"
          >예금 적금</RouterLink>
        <RouterLink to="/ExchangeRate" class="navLink"
          >환율</RouterLink>
        <RouterLink to="/map" class="navLink"
          >은행 Map</RouterLink>
        <RouterLink to="/market/gold" class="navLink"
          >상품 시세</RouterLink>
        <RouterLink to="/stock/Kospi" class="navLink"
          >주가 지수 시세</RouterLink>
        <RouterLink to="/recommend" class="navLink"
        >추천</RouterLink>
        <RouterLink to="/article" class="navLink"
        >게시판</RouterLink>
      </PopoverGroup>
      <div class="hidden lg:flex gap-2">
        <AuthBtn/>
        <DarkModeSwitch/>
      </div>
    </nav>

    <Dialog as="div" class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
      <div class="fixed inset-0 z-10" />
      <DialogPanel class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto  px-6 py-6 sm:max-w-sm sm:ring-1 
      bg-slate-800  sm:ring-gray-900/10
        dark:bg-slate-900 text-white dark:sm:ring-gray-100/10">
        <div class="flex items-center justify-between">
          <RouterLink to="/" class="-m-1.5 p-1.5 flex justify-center items-center">
            <h2 class="hidden">SSInvest</h2>
            <img src="../../assets/img/Logo/LogoImg.png" alt="Logo" class="h-10">
            <img src="../../assets/img/Logo/LogoWord.png" alt="Logo" class="h-6 lg:hidden xl:block">
          </RouterLink>
          <button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-500" @click="mobileMenuOpen = false">
            <span class="sr-only">Close menu</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-6">
              <RouterLink to="/bank" class="dialogLink"
                >예금 적금</RouterLink>
              <RouterLink to="/ExchangeRate" class="dialogLink"
                >환율</RouterLink>
              <RouterLink to="/map" class="dialogLink"
                >내 주위 은행 찾기</RouterLink>
              <RouterLink to="/market" class="dialogLink"
                >상품 시세</RouterLink>
              <RouterLink to="/stock" class="dialogLink"
                >주가 지수 시세</RouterLink>
              <RouterLink to="/recommend" class="dialogLink"
                >추천</RouterLink>
              <RouterLink to="/article" class="dialogLink"
                >게시판</RouterLink>
            </div>
            <div class="py-6 flex gap-2">
              <AuthBtn/>
              <DarkModeSwitch/>
            </div>
          </div>
        </div>
      </DialogPanel>
    </Dialog>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Dialog,
  DialogPanel,
  PopoverGroup,
} from '@headlessui/vue';
import {
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/vue/24/outline';

import AuthBtn from '../Auth/AuthBtn.vue'
import DarkModeSwitch from '../DarkModeSwitch.vue'
const mobileMenuOpen = ref(false)
</script>

<style lang="scss" scoped>
.navLink {
  @apply text-sm font-semibold leading-6;
  
}
.navLink:hover{
  transform: scale(1.2);
}

.dialogLink{
  @apply -mx-3 block rounded-lg px-3 py-2 
  text-base font-semibold leading-7 
  hover:bg-gray-900
  dark:hover:bg-gray-950;
}
</style>