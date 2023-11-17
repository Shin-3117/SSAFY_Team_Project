import config from "@/config"
import axios from "axios"
import { useAuthStore } from '../stores/auth';

const API_URL = config.baseURL
const authStore = useAuthStore()

export const userInfo = async (username:string) => {
  try{
    const response = await axios({
      method: 'get',
      url: `${API_URL}/users/profile/${username}/`
    })
    console.log(response)
    return response.data
  } catch(error){
    console.error(error);
  }
}

export const deleteUser = async () => {
  try{
    const response = await axios({
      method: 'post',
      url: `${API_URL}/users/delete_user/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    console.log(response)
    await authStore.logOut()
    // return response.data
  } catch(error){
    console.error(error);
  }
}

export const followUser = async () => {
  try{
    const response = await axios({
      method: 'post',
      url: `${API_URL}/users/follow/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
    console.log(response)
    await authStore.logOut()
    // return response.data
  } catch(error){
    console.error(error);
  }
}