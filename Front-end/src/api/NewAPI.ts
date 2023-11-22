import axios from 'axios';
import config from '@/config';

interface New{
  "id": number, 
  "title": string, 
  "originallink": string, 
  "pubdate": string
}

const baseURL = config.baseURL+'/news'
/**
 * @returns 뉴스 정보 가져오기
 */
const getNews = async () => {
  try{
    const response = await axios.get(
      `${baseURL}/data/0/`, {
    })
    const data:New[] = response.data
    console.log(response)
    return data
  } catch(error){
    console.error(error)
  }
}
export default getNews