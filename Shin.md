# 이슈발생
<details>
<summary>2023.11.13 카카오 맵 API, Vue3 연동</summary>
<div markdown="1">

  ## 카카오 맵 API의 공식 문서가 바닐라 JS로 작성되어 있음
  해당 문제를 해결하기 위해, Kakao에서 제공한, [Vue 예시코드 참조](https://codesandbox.io/s/nervous-keldysh-87yxg)

  <details>
  <summary>간단하게 지도 불러 오기로 수정 => 하지만 Vue2 문법을 사용 중</summary>
  <div markdown="1">

    ```Vue
    <!-- src/componets/Map/MapVue2.vue  -->
    <template>
      <div>
        <div id="map"></div>
        
      </div>
    </template>

    <script>
    import { toRaw } from "vue";
    import config from '../../config/index.ts'
    export default {
      name: "KakaoMap",
      data() {
        return {
        };
      },
      mounted() {
        if (window.kakao && window.kakao.maps) {
          this.initMap();
        } else {
          const script = document.createElement("script");
          /* global kakao */
          script.onload = () => kakao.maps.load(this.initMap);
          script.src =
            `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${config.mapKey}`;
          document.head.appendChild(script);
        }
      },
      methods: {
        initMap() {
          const container = document.getElementById("map");
          const options = {
            center: new kakao.maps.LatLng(33.450701, 126.570667),
            level: 5,
          };
          //지도 객체를 등록합니다.
          //지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
          this.map = new kakao.maps.Map(container, options);
        },
      },
    };
    </script>

    <!-- Add "scoped" attribute to limit CSS to this component only -->
    <style scoped>
    #map {
      width: 400px;
      height: 400px;
    }
    </style>
    ```
  </div>
  </details>

  <details>
  <summary>Vue2 문법 => Vue3 script setup 문법으로 수정</summary>
  <div markdown="1">

    ```Vue
    <!-- src/componets/Map/MapVue2.vue  -->
    <template>
      <div>
        <div id="map"></div>
      </div>
    </template>

    <script setup>
    import { ref, onMounted } from 'vue';
    import config from '../../config/index.ts';

    let map = null;

    onMounted(() => {
      if (window.kakao && window.kakao.maps) {
        initMap();
      } else {
        const script = document.createElement('script');
        /* global kakao */
        script.onload = () => kakao.maps.load(initMap);
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${config.mapKey}`;
        document.head.appendChild(script);
      }
    });

    const initMap = () => {
      const container = document.getElementById('map');
      const options = {
        center: new kakao.maps.LatLng(33.450701, 126.570667),
        level: 5,
      };

      // 지도 객체를 등록합니다.
      // 지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
      map = new kakao.maps.Map(container, options);
    };
    </script>

    <!-- Add "scoped" attribute to limit CSS to this component only -->
    <style scoped>
    #map {
      width: 400px;
      height: 400px;
    }
    </style>
    ```
  </div>
  </details>

  ## TS로 수정 시도중

  ### CDN 처리
</div>
</details>