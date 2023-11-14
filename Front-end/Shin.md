# 이슈발생
<details>
<summary>2023.11.13 카카오 맵 API, Vue3 연동</summary>
<div markdown="1">

  ## 카카오 맵 API의 공식 문서가 바닐라 JS로 작성되어 있음
  해당 문제를 해결하기 위해, Kakao에서 제공한, [Vue 예시코드 참조](https://codesandbox.io/s/nervous-keldysh-87yxg)

1. 간단하게 지도 불러 오기로 수정 => 하지만 Vue2 문법을 사용 중
   - src/componets/Map/MapVue2.vue

2. Vue2 문법 => Vue3 script setup 문법으로 수정
    - src/componets/Map/MapBank.vue


  ### CDN 처리
  ```JS
  onMounted(async () => {
    //CDN이 이미 추가 된 경우
    if (window.kakao && window.kakao.maps) {
      initMap();
    } else {
    //CDN이 추가 되지 않은 경우
      // script 태그 제작 후, 추가
      const script = document.createElement('script');
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${config.mapKey}&libraries=services`;
      document.head.appendChild(script);

      script.onload = () => {
        kakao.maps.load(initMap);
      }
    }
  });
  ```

</div>
</details>


<details>
<summary>2023.11.14 은행 예적금 Data를 서버에 저장후, 프론트 통신</summary>
<div markdown="1">

### table tag를 쓰면 안되는 이유

</div>
</details>