import axios from 'axios';
import config from '@/config';
const API_BASE_URL = config.baseURL; // 백엔드 서버 주소

// 데이터 타입 정의
export interface KosdaqData {
  id: number;
  basDt: string;
  idxNm: string;
  clpr: number;
}

// 데이터를 가져오는 함수
export function getKosdaqData(): Promise<KosdaqData[]> {
  return axios.get<KosdaqData[]>(`${API_BASE_URL}/market/send_data/kosdaq/`).then(response => response.data);
}