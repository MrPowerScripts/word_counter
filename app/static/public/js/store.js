import { applyMiddleware, createStore, compose } from 'redux'
import logger from 'redux-logger'
import thunk from 'redux-thunk'
import combineReducers from './reducers/index.js'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export default createStore(
  combineReducers,
  composeEnhancers(
    applyMiddleware( thunk ) // add `, logger()` if you want redux logging messages in console.
  ))
