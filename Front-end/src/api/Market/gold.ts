import axios from 'axios';
import config from '@/config';
const API_BASE_URL = config.baseURL; // 백엔드 서버 주소

// Gold 데이터 타입 정의
export interface GoldData {
  id: number;
  basDt: string;
  itmsNm: string;
  clpr: number;
}

// Gold 데이터를 가져오는 함수
export function getGoldData(): Promise<GoldData[]> {
  return axios.get<GoldData[]>(`${API_BASE_URL}/market/send_data/gold/`).then(response => response.data);
}