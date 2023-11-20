/*
예금
{
  "id": 103,
  "fin_prdt_cd": {
    "id": 35,
    "fin_prdt_cd": "10120114700011",
    "kor_co_nm": "수협은행",
    "fin_prdt_nm": "헤이(Hey)정기예금",
    "etc_note": "-1인 다계좌 가능.\n 단, 합산금액 최대 2억원 이내\n-최저 10만원 이상",
    "join_deny": 1,
    "join_member": "실명의 개인",
    "join_way": "인터넷,스마트폰",
    "spcl_cnd": "없음"
  },
  "intr_rate_type": "S",
  "intr_rate_type_nm": "단리",
  "intr_rate": 4.2,
  "intr_rate2": 4.2,
  "save_trm": 6
}

적금
{
  "id": 144,
  "fin_prdt_cd": {
      "id": 50,
      "fin_prdt_cd": "01012000200000000003",
      "kor_co_nm": "주식회사 케이뱅크",
      "fin_prdt_nm": "코드K 자유적금",
      "etc_note": "가입금액: 1만원 이상 30만원 이하\n가입기간: 6개월, 1년, 2년, 3년 \n(1인 최대 3계좌)",
      "join_deny": 1,
      "join_member": "만 17세 이상 실명의 개인 및 개인사업자",
      "join_way": "스마트폰",
      "spcl_cnd": "금리우대 코드를 입력하는 경우 우대금리 적용"
  },
  "intr_rate_type": "S",
  "intr_rate_type_nm": "단리",
  "intr_rate": 4.4,
  "intr_rate2": 4.4,
  "save_trm": 36,
  "rsrv_type": "F",
  "rsrv_type_nm": "자유적립식"
}
*/
interface Fin_prdt_cd{
  "id": number,
  "fin_prdt_cd": string,
  "kor_co_nm": string,
  "fin_prdt_nm": string
  "etc_note": string,
  "join_deny": number,
  "join_member": string,
  "join_way": string,
  "spcl_cnd": string
}
export interface SavingType {
  "id": number,
  "fin_prdt_cd": Fin_prdt_cd
  "intr_rate_type": string,
  "intr_rate_type_nm": string,
  "intr_rate": number,
  "intr_rate2": number,
  "save_trm": number,
  "is_subscribed":null|boolean
  "rsrv_type"?: string,
  "rsrv_type_nm"?: string
}

export interface BankDataType {
  "count": number,
  "page": number,
  "next": string|null,
  "previous": null|string,
  "results": SavingType[]
}