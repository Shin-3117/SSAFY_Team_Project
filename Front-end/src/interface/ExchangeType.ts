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