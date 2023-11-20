import axios from 'axios';
import config from '@/config';
// import { useAuthStore } from '@/stores/auth';

const baseURL = config.bankUrl
// const authStore = useAuthStore()
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
export const getBankList = async (Saving='deposit', term='0', sort_field='intr_rate',page=1) => {
  try{
    const response = await axios.get(
      `${baseURL}/${Saving}/${term}/${sort_field}/`, {
        params:{page:page}
      }
    )
    // console.log(response)
    response.data.page = page
    response.data.path = `/finlife/${Saving}/${term}/${sort_field}/`
    return response.data
  } catch(error){
    console.error(error)
  }
}

/**
 * @param {string} Saving (예금, 적금)['deposit', 'saving']
 * @returns 예금,적금 즐겨찾기
 */
export const postDeposit = async (
  product_id:number, option_id:number, page=1, path:string, token:string) => {
  try{
    const response = await axios.post(
      `${baseURL}/subscribe_deposit/`, {
        deposit_product: product_id,
        deposit_option: option_id,
        page:page,
        path: path
      },{
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    )
    console.log(response)
    // return response.data
  } catch(error){
    console.error(error)
  }
}

/**
 * @param {string} Saving (예금, 적금)['deposit', 'saving']
 * @returns 예금,적금 즐겨찾기
 */
export const postSaving = async (
  product_id:number, option_id:number, page=1, path:string,token:string) => {
  try{
    const response = await axios.post(
      `${baseURL}/subscribe_saving/`, {
        saving_product: product_id,
        saving_option: option_id,
        page:page,
        path:path
      },{
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    )
    console.log(response)
    // return response.data
  } catch(error){
    console.error(error)
  }
}