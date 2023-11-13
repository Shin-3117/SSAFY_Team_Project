<template>
  <div>
    <div id="map"></div>
    <div class="button-group">
      <button @click="changeSize(0)">Hide</button>
      <button @click="changeSize(400)">show</button>
      <button @click="displayMarker(markerPositions1)">marker set 1</button>
      <button @click="displayMarker(markerPositions2)">marker set 2</button>
      <button @click="displayMarker([])">marker set 3 (empty)</button>
      <button @click="displayInfoWindow">infowindow</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, toRaw } from "vue";
import config from '../../config/index.ts'
const markerPositions1 = ref( [
        [33.452278, 126.567803],
        [33.452671, 126.574792],
        [33.451744, 126.572441],
      ])
const markerPositions2 = ref([
        [37.499590490909185, 127.0263723554437],
        [37.499427948430814, 127.02794423197847],
        [37.498553760499505, 127.02882598822454],
        [37.497625593121384, 127.02935713582038],
        [37.49629291770947, 127.02587362608637],
        [37.49754540521486, 127.02546694890695],
        [37.49646391248451, 127.02675574250912],
      ])
const markers = ref([])
const infowindow = ref(null)

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