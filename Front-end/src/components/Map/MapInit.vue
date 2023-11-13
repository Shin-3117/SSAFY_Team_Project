<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, toRaw } from "vue";
import config from '../../config/index.js'


const self = this
onMounted(() => {
    if (window.kakao && window.kakao.maps) {
      self.initMap();
    } else {
      const script = document.createElement("script");
      /* global kakao */
      script.onload = () => kakao.maps.load(self.initMap);
      script.src =
        `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${config.mapKey}`;
      document.head.appendChild(script);
    }
  })
</script>

<style scoped>

</style>