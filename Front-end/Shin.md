# 이슈발생

## 2023.11.13
<details>
<summary>2023.11.13 카카오 맵 API, Vue3 연동</summary>
<div markdown="1">

  ### 카카오 맵 API의 공식 문서가 바닐라 JS로 작성되어 있음
  해당 문제를 해결하기 위해, Kakao에서 제공한, [Vue 예시코드 참조](https://codesandbox.io/s/nervous-keldysh-87yxg)

1. 간단하게 지도 불러 오기로 수정 => 하지만 Vue2 문법을 사용 중
   - src/componets/Map/MapVue2.vue

2. Vue2 문법 => Vue3 script setup 문법으로 수정
    - src/componets/Map/MapBank.vue


  #### CDN 처리
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

## 2023.11.14
<details>
<summary>2023.11.14 은행 예적금 Data를 서버에 저장후, 프론트 통신</summary>
<div markdown="1">

### CORS 처리
장고에서 `corsheaders`라이브러리를 이용하여 Header 부분에 `CORS_ALLOWED_ORIGINS` 추가
```python
# settings.py
INSTALLED_APPS = [
    ...,
    'corsheaders',
    ...,
]

MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...,
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]
```

### 통신 Data TS interface로 Type 정의

`/src/interface/BankData.ts`에 데이터 타입 정의

Type import의 경우 `import type SavingType from '@/interface/BankData'`
형식으로 `import type` 사용

import한 Type 적용
```TS
import type SavingType from '@/interface/BankData'

const depositList = ref<SavingType[] | null>(null);
const isModalOpen = ref({
  state: false,
  data: null as SavingType | null,
})
```

#### Data Table
`BankDeposit.vue`컴포넌트에서 
table tag에서 article, div tag로 변경

##### table tag를 쓰면 안되는 이유
웹표준을 지키는 것과 테이블 레이아웃은 별개의 문제

웹 접근성을 지키기 위해서 테이블을 쓰지 말라는 것

</div>
</details>

## 2023.11.15
<details>
<summary>2023.11.15 로그인 토큰 처리, 환율 기능 세팅</summary>
<div markdown="1">

### 로그인 토큰 처리
BE 장고에서 dj-rest-auth 사용하여 setting
```bash
pip install dj-rest-auth
```
```python
# settings.py
INSTALLED_APPS = [
    ...
    'dj_rest_auth',
    ...
]

# project/urls.py
urlpatterns = [
    ...
    path('accounts/', include('dj_rest_auth.urls')),
]
```

추후 추가 기능 : Registration 기능 추가 
```bash
pip install 'dj-rest-auth[with_social]'
```

FE에서는 로그인 후, Header에 포함된 token을 
pinia로 stores/auth.ts에 관리 저장 및 로그인 상태 관리

Axios 통신을 할 때, data의 key값을 완전히 일치해 줘야하고,
로그인과 회원가입 요청의 data key 값이 다음
```TS
export interface LogInInfo{
  username:string,
  password:string,
}

export interface SignUpInfo{
  username:string,
  password1:string,
  password2:string
}
```

### 환율기능 세팅
BE에서 통신 받은 데이터를 JSDoc으로 설명 및 타입 정의 하여 데이터를 받음
```TS
/**
 * "cur_unit": 국가코드
 * 
 * "cur_nm": 국가이름
 * 
 * "deal_bas_r": 1외화가 한화로 얼마인지
 * 
 * "krw_to_cur": 1000원으로 외화
 */
export default interface ExchangeType{
  "id": number, 
  "cur_unit": string, 
  "cur_nm": string, 
  "ttb": string, 
  "tts": string, 
  "deal_bas_r": string|number, 
  "krw_to_cur": string|number, 
  "req_dt": string
}
```
환율 계산에 사용하는 "deal_bas_r", "krw_to_cur" 키는 FE에서 
string을 parseFloat를 통해 number 타입으로 변환하여 사용합니다.

현제 TS error 가 발생하는 관계로 수정 필요

</div>
</details>