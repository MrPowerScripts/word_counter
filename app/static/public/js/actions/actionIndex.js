import { bindActionCreators } from 'redux'

import * as baseActions from './baseActions'

export default function bindActions(dispatch) {
  return (bindActionCreators({...baseActions}, dispatch))
}
