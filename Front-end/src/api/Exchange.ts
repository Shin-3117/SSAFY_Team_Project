import axios from 'axios';
import config from '@/config';

const baseURL = config.exchangeUrl
/**
 * country (국가코드)
 *
 * @param {string} country
 * @returns 국가별 환율 정보
 */
const getExchange = async (country='ALL') => {
  try{
    const response = await axios.get(
      `${baseURL}/info/${country}/`, {
    })
    // console.log(response)
    return response.data
  } catch(error){
    console.error(error)
  }
}
export default getExchange