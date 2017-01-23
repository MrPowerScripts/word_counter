import React from 'react'
import { connect } from 'react-redux'
import { browserHistory, Link } from 'react-router'
import actions from '../actions/actionIndex'

@connect(
  store => {return {...store}},
  dispatch => ({actions : actions(dispatch)}))
export default class App extends React.Component{

  constructor() {
    super()

    this.state = {
      recentlyUpdated: [],
      updatedLoaded: false
    }
  }

  componentDidMount() {
    wordCore.getRecentlyUpdated()
    .success(success => {
      this.setState({
        recentlyUpdated: success.success,
        updatedLoaded: true
      })
    })
  }

  submitUrl = (event) => {
    // Don't refresh the page, this isn't 1995
    event.preventDefault()

    wordCore.submitUrl(this.refs.urlInput.value)
    .success(success => {
      browserHistory.push(`/url/${success.url}`)
    })
  }

  getRecentlyUpdatedNodes = (data) => {
    return (
      data.map(url => {
        return (
          <Link to={`/url/${url.url}`}>
            <div className="last-updated-item">{url.url}</div>
          </Link>
        )
      })
    )
  }

  render () {

    return (
      <div className="main">
        <form className="input-form" onSubmit={this.submitUrl}>
          <input ref="urlInput"
            placeholder="website to fetch"
            className="url-input"
            type="url"
            required />
            <button type="submit" className="url-submit button">Fetch</button>
        </form>
        {this.state.updatedLoaded &&
          <div className="last-updated">
            <h3>Last Updated</h3>
            {this.getRecentlyUpdatedNodes(this.state.recentlyUpdated)}
          </div>
        }
      </div>
    )
  }
};
