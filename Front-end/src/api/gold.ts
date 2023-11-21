import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; // 백엔드 서버 주소

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