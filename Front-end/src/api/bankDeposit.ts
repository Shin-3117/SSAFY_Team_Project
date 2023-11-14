import axios from 'axios';
import config from '@/config';

const baseURL = config.bankUrl
/**
 * term (저축기간): [6, 12, 24, 36]
 * 
 * sort_field (기본금리, 우대금리): ['intr_rate', 'intr_rate2']
 * 
 * Saving (예금, 적금) : ['deposit', 'saving']
 * @param {number} term
 * @param {string} sort_field
 * @returns 은행 예금, 적금 리스트
 */
const getBankList = async (Saving='deposit', term=6, sort_field='intr_rate') => {
  try{
    const response = await axios.get(
      `${baseURL}/${Saving}/${term}/${sort_field}/`, {
    })
    // console.log(response.data)
    // console.log(response.data.result.baseList)
    // console.log(response.data.result.optionList)
    return response.data
  } catch(error){
    console.error(error)
  }
}
export default getBankList