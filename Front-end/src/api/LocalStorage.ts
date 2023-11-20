/* Local Storage
반영구적으로 브라우저에 데이터를 저장할 수 있는 공간
-> 브라우저를 껐다 켜도 데이터 유지

브라우저 별로 용량은 다르지만 크롬기준 5MB정도 저장가능

직접 조회가 가능하기 때문에 보안 좋진 않음
-> 위험 수준이 낮은 데이터만 저장

value에는 문자열만 저장 가능
-> json으로 저장
*/

/**localStorage에 data 저장 */ 
export const addLocalStorage = (key:string, value:string|Object) => {
  if (typeof(value)==='string'){
    localStorage.setItem(key, value)
  } else if (typeof(value)==='object'){
    // JSON으로 변환
    localStorage.setItem(key, JSON.stringify(value))
  }
}

/**localStorage 값 가져오기 */ 
export const getLocalStorage = (key:string) => {
  const data = localStorage.getItem(key)
  if (typeof(data)==='string'){
    const objData = JSON.parse(data)
    return objData
  } else {
    return null
  }
}