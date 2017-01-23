import React from 'react'
import ReactDOM from 'react-dom'

import App from './App.jsx'
import Site from './Site.jsx'
import Base from './Base.jsx'

import { Router, Route, IndexRoute, Link, browserHistory, applyRouterMiddleware } from 'react-router'
import { Provider } from 'react-redux'
import { useScroll } from 'react-router-scroll'
import { syncHistoryWithStore } from 'react-router-redux'


import store from '../store.js'

const history = syncHistoryWithStore(browserHistory, store)

ReactDOM.render((
<Provider store={store}>
  <Router history={history} render={applyRouterMiddleware(useScroll())}>
    <Route component={Base}>
      <Route path='/' component={App}/>
      <Route path='/url/:site' component={Site}/>
    </Route>
  </Router>
</Provider>
), document.getElementById('root'));
