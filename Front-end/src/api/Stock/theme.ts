import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; // 백엔드 서버 주소

// 데이터 타입 정의
export interface ThemeData {
  id: number;
  basDt: string;
  idxNm: string;
  clpr: number;
}

// 데이터를 가져오는 함수
export function getThemeData(): Promise<ThemeData[]> {
  return axios.get<ThemeData[]>(`${API_BASE_URL}/market/send_data/theme/`).then(response => response.data);
}