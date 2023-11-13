//https://finlife.fss.or.kr/finlife/api/fdrmDpstApi/list.do?menuNo=700052
//http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={발급받은 인증키}&topFinGrpNo=020000&pageNo=1
import config from '../config';
import axios from 'axios';

const baseURL = config.apiUrl;
const key = config.apiKey;

/**
 * topFinGrpNo (금융회사가 속한 권역 코드): default = '020000'
 * 020000(은행), 030300(저축은행), 030200(여신전문), 050000(보험), 060000(금융투자)
 * 
 * @param {string} topFinGrpNo 
 * @param {number} pageNo 
 * @returns 
 */
const getDepositList = async (topFinGrpNo='020000', pageNo=1) => {
  try{
    const response = await axios.get(
      `${baseURL}/finlifeapi/depositProductsSearch.json`, {
        // headers: {
        //   'Access-Control-Allow-Origin': '*',
        // }, 안됨
        params: {
          auth: key,
          topFinGrpNo: topFinGrpNo,
          pageNo: pageNo
        }
    })
    // console.log(response.data)
    // console.log(response.data.result.baseList)
    // console.log(response.data.result.optionList)
    return response.data
  } catch(error){
    console.error(error)
  }
}
export default getDepositList

/*
{
  "result": {
    "prdt_div": "D",
    "total_count": 366,
    "max_page_no": 4,
    "now_page_no": 1,
    "err_cd": "000",
    "err_msg": "정상",
    "baseList": [],
    "optionList": []
  }
}
{
  dcls_month: '202310',
  fin_co_no: '0010001',
  fin_prdt_cd: 'WR0001B',
  kor_co_nm: '우리은행',
  fin_prdt_nm: 'WON플러스예금',
  join_way: '인터넷,스마트폰,전화(텔레뱅킹)',
  mtrt_int: '만기 후\n' +
    '- 1개월이내 : 만기시점약정이율×50%\n' +
    '- 1개월초과 6개월이내: 만기시점약정이율×30%\n' +
    '- 6개월초과 : 만기시점약정이율×20%\n' +
    '\n' +
    '※ 만기시점 약정이율 : 일반정기예금 금리',
  spcl_cnd: '해당사항 없음',
  join_deny: '1',
  join_member: '실명의 개인',
  etc_note: '- 가입기간: 1~36개월\n' +
    '- 최소가입금액: 1만원 이상\n' +
    '- 만기일을 일,월 단위로 자유롭게 선택 가능\n' +
    '- 만기해지 시 신규일 당시 영업점과 인터넷 홈페이지에 고시된 계약기간별 금리 적용',
  max_limit: null,
  dcls_strt_day: '20231020',
  dcls_end_day: null,
  fin_co_subm_day: '202310200948'
}
{
  dcls_month: '202310',
  fin_co_no: '0010001',
  fin_prdt_cd: 'WR0001B',
  intr_rate_type: 'S',
  intr_rate_type_nm: '단리',
  save_trm: '6',
  intr_rate: 4.02,
  intr_rate2: 4.02
} */