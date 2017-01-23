import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import base from './baseReducers';


export default combineReducers({
  routing: routerReducer,
  base
})
