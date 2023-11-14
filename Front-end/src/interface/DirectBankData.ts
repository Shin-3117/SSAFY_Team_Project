interface BankBase {
  dcls_month: string;
  fin_co_no: string;
  fin_prdt_cd: string;
  kor_co_nm: string;
  fin_prdt_nm: string;
  join_way: string;
  mtrt_int: string;
  spcl_cnd: string;
  join_deny: string;
  join_member: string;
  etc_note: string;
  max_limit: null | string;
  dcls_strt_day: string;
  dcls_end_day: null | string;
  fin_co_subm_day: string;
}

interface BankOption {
  dcls_month: string;
  fin_co_no: string;
  fin_prdt_cd: string;
  intr_rate_type: string;
  intr_rate_type_nm: string;
  save_trm: string;
  intr_rate: null | number;
  intr_rate2: number;
}

interface BankResult {
  prdt_div: string;
  total_count: number;
  max_page_no: number;
  now_page_no: number;
  err_cd: string;
  err_msg: string;
  baseList: BankBase[];
  optionList: BankOption[];
}