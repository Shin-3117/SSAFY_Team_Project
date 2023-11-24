<template>
<div class="md:flex md:items-start animate-fade animate-duration-[1000ms]">
  <div class="container p-4 border-2 mt-4 mr-2 rounded-lg border-indigo-400">
    <div class="flex border-2 p-1 rounded-lg border-indigo-300">
      <select v-model="select.city" 
        class="p-2 cursor-pointer border border-indigo-300 rounded 
        bg-white dark:bg-gray-800">
        <option value="" disabled>Select City</option>
        <option v-for="(city, key) in placeInfo" :key="key" :value="key">{{ key }}</option>
      </select>
      <div>
        <select v-model="select.gu" 
          class="p-2  cursor-pointer border border-indigo-300 rounded
          bg-white dark:bg-gray-800" >
          <option value="" disabled>Select District</option>
          <option v-for="(place, gu) in placeInfo[select.city]" :key="gu" :value="gu"
          >{{ gu }}</option>
        </select>
      </div>
    </div>
    <div class="mt-4">
      <p class="text-lg font-bold">Selected: {{ select.city }} - {{ select.gu }}</p>
      <div class="flex justify-between">
        <button class="Radio"
          @click="moveMap(select.lat, select.long)"
        >위치로 이동 </button>
        <button class="Radio"
          @click="reSearch()"
          >현재 위치에서 검색 </button>
      </div>
    </div>
    <div id="map"></div>
  </div>
  <div class="p-4 border-2 border-indigo-400 rounded-lg mt-4 w-96">
    <h2 class="text-lg font-bold border-2 p-3 rounded-xl border-indigo-300">검색결과</h2>
    <br>
    <div class="border-2 p-3 rounded-xl border-indigo-300">
    <ul v-if="searchList">
      <li v-for="result in searchList" class="py-1 animate-fade">
        {{ result }}
      </li>
    </ul>
    </div>
  </div>

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

const updateSelectedGu = () => {
  select.value.lat = placeInfo[select.value.city][select.value.gu].lat;
  select.value.long = placeInfo[select.value.city][select.value.gu].long;
};

let map = null;
let infowindow = null;
let ps = null;
let markers = []
const searchList = ref([])

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

const moveMap = ()=>{
  updateSelectedGu()
  let lat = parseFloat(select.value.lat)
  let long = parseFloat(select.value.long)

  let moveLatLon = new kakao.maps.LatLng(lat,long);
  
  // 지도 중심을 부드럽게 이동시킵니다
  // 만약 이동할 거리가 지도 화면보다 크면 부드러운 효과 없이 이동합니다
  map.panTo(moveLatLon);

  deleteMarkers()
  infowindow = new kakao.maps.InfoWindow({zIndex:1})
  ps = new kakao.maps.services.Places(map);
  ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true});
}

const reSearch = ()=>{
  const {La, Ma} = map.getCenter()
  let moveLatLon = new kakao.maps.LatLng(Ma,La);
  deleteMarkers()
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
  } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.');
    return;
  } else if (status === kakao.maps.services.Status.ERROR) {
    alert('검색 결과 중 오류가 발생했습니다.');
    return;
  }
}
// 지도에 마커를 표시하는 함수입니다
const displayMarker = (place) => {
    // 마커를 생성하고 지도에 표시합니다
    const marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x) 
    });
    markers.push(marker)
    // console.log(markers)
    // 마커에 클릭이벤트를 등록합니다
    kakao.maps.event.addListener(marker, 'click', function() {
        // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
        infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
        infowindow.open(map, marker);
    });
    // kakao.maps.event.addListener(marker, 'mouseover', function() {
    //     infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
    //     infowindow.open(map, marker);
    // });
    // kakao.maps.event.addListener(marker, 'mouseout', function() {
    //   infowindow.close();
    // });
    // itemEl.onmouseover =  function () {
    //     infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
    //     infowindow.open(map, marker);
    // };
    // itemEl.onmouseout =  function () {
    //     infowindow.close();
    // };

    searchList.value.push(place.place_name)
}

const deleteMarkers = () => {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null); 
  }
  markers = []
  searchList.value = []
}

onMounted(async () => {
  if (window.kakao && window.kakao.maps) {
    initMap(); 
    // console.log('scrit add ok')
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
  margin-top: 12px;
}
.container{
  width: 440px;
}
.Radio{
  @apply cursor-pointer bg-indigo-400 hover:bg-gradient-to-br from-purple-600 to-blue-500 
  text-white font-bold py-2 px-4 rounded-md mr-1;
}
</style>
