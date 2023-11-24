# 이슈발생

## 2023.11.13 월
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

## 2023.11.14 화
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

## 2023.11.15 수
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

## 2023.11.16 목
<details>
<summary>2023.11.16 회원가입 입력정보 수정, 카카오맵 api으로 은행 검색 기능 구현 </summary>
<div markdown="1">

### 회원가입 입력정보 수정
- 기존에는 회원가입 시, {아이디, 비밀번호, 비밀번호확인}을 서버로 전송했지만,

  서버 구조 변경으로 {아이디, 비밀번호, 비밀번호확인, 성별, 생년월일, 보유자산}으로 변경

  src/interface/AuthType
  ```TS
  export interface SignUpInfo{
    username:string,
    password1:string,
    password2:string,
    gender:number,
    birthday:string,
    money:number
  }
  ```

- 회원가입 시, 양식에 만족하지 못하는 data로 서버요청이 안 가도록 방어코드, 에러문구 작성

### 카카오맵 api으로 은행 검색 기능 구현
/src/components/Map/MapBankList
#### 1. 위치 선택 후, 해당 위치로 이동 기능
placeInfo.json에 시군구의 위도, 경도 값을 저장하고 이를 컴포넌트에서 사용

초기에는 해당 위치를 map의 center하는 지도 생성하여 구현

#### 1-1. (오류) 지도가 겹쳐지는 
카카오 맵 api에서는 맵을 하나만 생성하고 HTML tag에 mount하는 방식

하지만, 맵을 하나만 생성하는 것이 아닌 맵을 계속 새로 만드는 방식으로 코드를 구현하여 오류발생

수정을 위해 초기에 컴포넌트가 생성될 때, 1회만 맵을 생성하고, 맵을 조작하는 방식으로 변경시킴

#### 1-2. 맵 조작
  ```JS
  const moveMap = (lat,long)=>{
    lat = parseFloat(lat)
    long = parseFloat(long)
    let moveLatLon = new kakao.maps.LatLng(lat,long);
    
    // 지도 중심을 부드럽게 이동시킵니다
    // 만약 이동할 거리가 지도 화면보다 크면 부드러운 효과 없이 이동합니다
    map.panTo(moveLatLon);

    // 기존의 마커 삭제
    deleteMarkers()
    // 은행 검색 및 결과 처리
    infowindow = new kakao.maps.InfoWindow({zIndex:1})
    ps = new kakao.maps.services.Places(map);
    ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true});
  }
  ```

#### 2. 지도에서 보고있는 화면에서 은행 검색
1번의 방식으로는 보고있는 지도를 사용자가 이동시켰을 때, 추가적인 마커를 생성하지 않음

또한, 해당 지도에서 은행 검색이 불가능

이를 해결하기 위해, 지도에서 보고있는 화면에서 은행 검색 기능 구현

사용자가 보고있는 화면의 경도 위도 정보를 받고,
이 정보를 바탕으로 재검색할 수 있는 버튼 추가

#### 2-1. (오류) 마커가 겹쳐져서 계속 생성됨
재검색시 기존에 생성한 마커가 사라지지 않고, 계속 생성이됨

  이를 위해 마커를 배열에 모으고, 마커들을 제거하는 함수생성
  ```JS
  let markers = []

  //... 마커 생성 후, markers.push(marker)

  const deleteMarkers = () => {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null); 
    }
    markers = []
  }
  ```

</div>
</details>

## 2023.11.17 금
<details>
<summary>2023.11.17 게시판, 댓글 기능 구현</summary>
<div markdown="1">

### 게시판 기능
전체 게시판을 조회하는 ArticleView
-게시글을 생성하는 MakeArticleView
-상세 게시글을 조회하는 ArticleDetailView
--게시글 수정하는 PutArticleView

1. 게시글 생성, 게시글 수정의 경우 View를 만들어 라우터를 연결하는 것이 아닌
컴포넌트로 구현하는 방법도 생각했으나,

컴포넌트의 경우, 사용자들이 뒤로가기 버튼을 사용시 문제가 발생하므로 View로 제작

2. 게시글 수정의 경우, 게시글 생성과 유사하여 하나의 View로 구현하는 방법도 고려했지만,

기능별로 분류해주는 것이 나중에 유지관리에 좋을 것으로 생각되어 분리하여 제작

3. 게시글 수정에서 ArticleDetailView에서 조회한 데이터를 PutArticleView로 넘기게 수정할 필요가 있음
   현재는 PutArticleView에서 다시 서버에 요청하여 데이터를 받음

### 댓글 기능 구현
- 댓글 생성 
- 댓글 수정 
- 댓글 삭제 
- 대댓글 생성 
- 대댓글 수정 
- 대댓글 삭제
  완료
  수정의 경우, 수정 버튼을 누르면 수정 할수 있는 input 출력
  placeholder가 아닌 값으로 수정하기 편하게 수정할 필요가 있음
  -> v-model이 아닌 :value @input 로 바인딩 필요할 것으로 보임
</div>
</details>

## 2023.11.18 토
<details>
<summary>2023.11.18 유저 팔로우, 게시판 작성시간 추가</summary>
<div markdown="1">

### 유저 팔로우
```TS
export const followUser = async (username:string) => {
  try{
    const response = await axios({
      method: 'post',
      url: `${API_URL}/users/follow/${username}/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    // console.log(response)
    alert('follow')
  } catch(error){
    console.error(error);
  }
}
```
토큰을 통해 인증 처리

### 게시판 작성시간 추가
전체 게시판 data에 작성시간 추가 및 프론트에 반영 

</div>
</details>

## 2023.11.19 일
<details>
<summary>2023.11.19 세션 스토리지에 토큰 저장 기능 구현</summary>
<div markdown="1">

0. stores/auth에서 회원정보를 관리 중.
1. 로그인을 진행시, 토큰을 세션 스토리지에 저장
2. 새로고침을 진행해도 세션 스토리지로 로그인 상태를 유지
3. 로그아웃, 브라우져 종료시 세션 스토리지 삭제 및 로그아웃

</div>
</details>

## 2023.11.20 월
<details>
<summary>2023.11.19 게시판 좋아요 기능 구현, 예적금 페이지 페이지네이션, 예적금 즐겨찾기 기능 구현</summary>
<div markdown="1">

### 게시판 좋아요 기능 구현
아이콘 이미지(좋아요)클릭 시, 좋아요 구현

### 예적금 페이지 페이지네이션
0. 기존에는 예적금 data를 모두 받아왔음
1. page개념 도입 제안, 1page 당, data를 20개씩 받도록 수정
2. 페이지 네이션 기능 추가

### 예적금 즐겨찾기 기능 구현
로그인 상태인 경우, 즐겨찾기 토글(아이콘) 출력
즐겨찾기 기능 구현

</div>
</details>

## 2023.11.21 화
<details>
<summary>2023.11.21 예적금 즐겨찾기 기능 캐싱 처리, 게시글 좋아요 토글 처리</summary>
<div markdown="1">

### 예적금 즐겨찾기 기능 캐싱 처리
0. 즐겨찾기를 해도 캐싱으로 인해 최신화된 데이터가 들어오지 않음
1. axios요청시, body에 path를 추가하여 캐싱 초기화 및 최신화된 데이터 반환
2. 즐겨찾기 유무로 즐겨찾기 아이콘 표시

</div>
</details>