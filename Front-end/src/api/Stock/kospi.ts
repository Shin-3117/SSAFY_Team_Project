import axios from 'axios';
import config from '@/config';
const API_BASE_URL = config.baseURL; // 백엔드 서버 주소

// 데이터 타입 정의
export interface KospiData {
  id: number;
  basDt: string;
  idxNm: string;
  clpr: number;
}

// 데이터를 가져오는 함수
export function getKospiData(): Promise<KospiData[]> {
  return axios.get<KospiData[]>(`${API_BASE_URL}/market/send_data/kospi/`).then(response => response.data);
}