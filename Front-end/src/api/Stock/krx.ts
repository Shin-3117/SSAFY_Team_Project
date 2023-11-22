import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; // 백엔드 서버 주소

// 데이터 타입 정의
export interface KrxData {
  id: number;
  basDt: string;
  idxNm: string;
  clpr: number;
}

// 데이터를 가져오는 함수
export function getKrxData(): Promise<KrxData[]> {
  return axios.get<KrxData[]>(`${API_BASE_URL}/market/send_data/krx/`).then(response => response.data);
}