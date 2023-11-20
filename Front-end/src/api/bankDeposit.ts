import axios from 'axios';
import config from '@/config';

const baseURL = config.bankUrl
/**
 * term (저축기간): [0, 6, 12, 24, 36]
 * 
 * sort_field (기본금리, 우대금리): ['intr_rate', 'intr_rate2']
 * 
 * Saving (예금, 적금) : ['deposit', 'saving']
 * @param {number} term
 * @param {string} sort_field
 * @returns 은행 예금, 적금 리스트
 */
const getBankList = async (Saving='deposit', term='0', sort_field='intr_rate',page=1) => {
  try{
    const response = await axios.get(
      `${baseURL}/${Saving}/${term}/${sort_field}/`, {
        params:{page:page}
      }
    )
    console.log(response)
    return response.data
  } catch(error){
    console.error(error)
  }
}
export default getBankList