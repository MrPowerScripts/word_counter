import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'

@connect((store) => {
  return {
    ...store
  }
})
export default class Base extends React.Component{

  componentWillMount() {
  }

  render () {
    return (
      <div className="base-container">
        <div className="base">
          <div className="nav">
            <Link className="nav-action" to="/">Home</Link>
          </div>
          {this.props.children}
        </div>
      </div>
    )
  }
}
