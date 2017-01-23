import { normalize } from 'normalizr'
import { sitesSchema } from '../normalizrSchemas/baseSchemas'

export default function reducer(state={
    siteData: {
      entities: { data: {}},
      result: []
    }
}, action) {
  switch (action.type) {
    case 'SET_URL_DATA':
      return {...state, siteData: normalize(action.payload, sitesSchema)}
    case 'CLEAR_URL_DATA':
      return {...state, siteData: {entities:{data:{}},result:[]}}
    default :
      return state
  }
}
