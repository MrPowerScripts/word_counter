export function setUrlData(data) {
  return  {
    type: 'SET_URL_DATA',
    payload: data
  }
}

export function clearUrlData() {
  return  {
    type: 'CLEAR_URL_DATA'
  }
}
