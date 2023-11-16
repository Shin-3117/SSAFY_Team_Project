<template>
  <div class="relative w-48">
    <ul v-for="(city, key) in placeInfo" :key="key">
      <li class="flex bg-slate-300">
        <p class="p-1" @click="setSelect(key)">{{ key }}</p>
        <div v-if="select.city===key" class="absolute top-0 right-0">
          <ul v-for="(place, gu) in city" :key="gu">
            <li class="p-1 bg-orange-500"
            @click="()=>{
              select.gu=gu; 
              select.lat=place.lat;
              select.long=place.long}"
            >{{ gu }}</li>
          </ul>
        </div>
      </li>
    </ul>
<p>{{ select }}</p>
<button class="bg-blue-400" 
@click="moveMap(select.lat, select.long)"
>지도보기</button>
    <div id="map"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import config from '../../config/index';
import placeInfo from './placeInfo.json'

const select = ref({
  city:null,
  gu:null,
  lat:37.4951,
  long:127.06278
})
const setSelect = (key) => {
  if(select.value.city === key){
    select.value.city = null
  } else {
    select.value.city = key
  }
}



let map = null;
let infowindow = null;
let ps = null;

const initMap = (lat=37.4951, long=127.06278) => {
  const container = document.getElementById('map');
  const options = {
    center: new kakao.maps.LatLng(lat, long),
    level: 7,
  };
  // 지도 객체를 등록합니다.
  // 지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
  map = new kakao.maps.Map(container, options);

  infowindow = new kakao.maps.InfoWindow({zIndex:1})
  ps = new kakao.maps.services.Places(map);
  ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true});
};

const moveMap = (lat,long)=>{
  lat = parseFloat(lat)
  long = parseFloat(long)
  console.log(lat,long)
  // initMap(lat,long)
  let moveLatLon = new kakao.maps.LatLng(lat,long);
  
  // 지도 중심을 부드럽게 이동시킵니다
  // 만약 이동할 거리가 지도 화면보다 크면 부드러운 효과 없이 이동합니다
  map.panTo(moveLatLon);  

  infowindow = new kakao.maps.InfoWindow({zIndex:1})
  ps = new kakao.maps.services.Places(map);
  ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true});
}

// 키워드 검색 완료 시 호출되는 콜백함수 입니다
const placesSearchCB = (data, status, pagination) => {
    if (status === kakao.maps.services.Status.OK) {
        for (let i=0; i<data.length; i++) {
            displayMarker(data[i]);    
        }       
    }
}
// 지도에 마커를 표시하는 함수입니다
const displayMarker = (place) => {
    // 마커를 생성하고 지도에 표시합니다
    const marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x) 
    });

    // 마커에 클릭이벤트를 등록합니다
    kakao.maps.event.addListener(marker, 'click', function() {
        // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
        infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
        infowindow.open(map, marker);
    });
}

onMounted(async () => {
  if (window.kakao && window.kakao.maps) {
    initMap(); 
    console.log('scrit add ok')
  } else {
    const script = document.createElement('script');
    /* global kakao */
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${config.mapKey}&libraries=services`;
    document.head.appendChild(script);
    script.onload = () => {
      kakao.maps.load(initMap);
    }
  }
});


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#map {
  width: 400px;
  height: 400px;
  margin: 20px;
}
</style>
