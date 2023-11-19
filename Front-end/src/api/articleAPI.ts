import axios from 'axios';
import config from '@/config';
import { useAuthStore } from '../stores/auth';


const baseURL = config.baseURL
const authStore = useAuthStore()


/**
 * @returns 게시글 전체 조회
 */
export const getArticles = async () => {
  try{
    const response = await axios.get(
      `${baseURL}/articles/`, {
    })
    // console.log(response)
    return response.data
  } catch(error){
    console.error(error)
  }
}

/**
 *
 * @param {number} article_id
 * @returns 게시글 상세 조회
 */
export const getArticle = async (article_id:number) => {
  try{
    const response = await axios.get(
      `${baseURL}/articles/${article_id}/`, {
    })
    // console.log(response)
    return response.data
  } catch(error){
    console.error(error)
  }
}

/**
 * @returns 게시글 생성
 */
export const postArticle = async (title:string, content:string) => {
  try{
    const response = await axios.post(
      `${baseURL}/articles/`, {
        "title": title,
        "content": content
    },{
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    console.log(response)

    return response.data
  } catch(error){
    console.error(error)
    return false
  }
}

/**
 * 
 * @param article_id 
 * @param title 
 * @param content 
 * @returns 게시글 수정
 */
export const putArticle = async (article_id:number, title:string, content:string) => {
  try{
    const response = await axios({
      method: 'put',
      url: `${baseURL}/articles/${article_id}/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
      data: {
        "title": title,
        "content": content
      }
    })
    return true
    // console.log(response)
    // return response.data
  } catch(error){
    console.error(error)
  }
}
/**
 * 
 * @param article_id 
 * @returns 게시글 삭제
 */
export const deleteArticle = async (article_id:number) => {
  try{
    const response = await axios({
      method: 'delete',
      url: `${baseURL}/articles/${article_id}/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    alert('삭제완료')
    return true
    // console.log(response)
    // return response.data
  } catch(error){
    console.error(error)
    alert('fail')
    return false
  }
}



/**
 * 
 * @param article_id 댓글이 작성된 게시글 아이디
 * @param content 댓글 내용
 * @param parent 대댓글 작성시 댓글 id
 */
export const postComment = async (article_id:number, content:string, parent=null) => {
  try{
    axios({
      method: 'post',
      url: `${baseURL}/articles/${article_id}/comments/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
      data: {
        "content": content,
        "parent": parent
      }
    })
  } catch(error) {
    console.error(error)
  }
}

/**
 * @param method ['delete', 'put', 'patch']
 * @param comment_id 댓글 아이디
 * @param content 댓글 내용
 */
export const apiComment = async (method:string, comment_id:number, content:string) => {
  try{
    axios({
      method: method,
      url: `${baseURL}/articles/comments/${comment_id}/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
      data: {
        "content": content,
      }
    })
  } catch(error) {
    console.error(error)
  }
}