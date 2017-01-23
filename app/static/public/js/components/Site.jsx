import React from 'react'
import { connect } from 'react-redux'
import { filter, orderBy } from 'lodash'
import moment from 'moment';
import actions from '../actions/actionIndex'

@connect(
  store => {return {...store}},
  dispatch => ({actions : actions(dispatch)}))
export default class Site extends React.Component{

  constructor(props) {
    super(props)

    this.state = {
      dataIds: props.base.siteData.result,
      data: props.base.siteData.entities.data,
      current_data: [],
      highValue: 0,
      lowValue: 0,
      totalValue: 0,
      selected: null
    }
  }

  componentWillMount() {
    this.props.actions.clearUrlData()
  }

  componentDidMount() {
    wordCore.getSiteData(this.props.params.site)
    .success(success => {
      this.props.actions.setUrlData(success.success)
    })
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      dataIds: nextProps.base.siteData.result,
      data: nextProps.base.siteData.entities.data
    })
  }

  refreshFetch = () => {
    wordCore.submitUrl(`http://${this.props.params.site}`)
    .success(success => {
      wordCore.getSiteData(this.props.params.site)
      .success(success => {
        this.props.actions.setUrlData(success.success)
      })
    })
  }

  selectData = (event) => {

    var words = this.state.data[parseInt(event.target.dataset.id)].word_counts

    // normalize counted items into key/value objects
    var words_fixed = Object.keys(words).map(key => {
      return {key: key, value: words[key]}
    })

    // sort the data based on the counter value
    words_fixed.sort((a, b) => {
      return b.value - a.value
    })

    // get the top 100 words
    var list = words_fixed.slice(0, 100)

    var wordGroups = []
    list.forEach(item => {

      if (!wordGroups.hasOwnProperty(item.value)) {
        wordGroups[item.value] = {words:[]}
      }

      wordGroups[item.value].words.push(item.key)
    })

    var normalizedGroups = Object.keys(wordGroups).map(key => {
      return (
        {count: parseInt(key), words: wordGroups[key].words}
      )
    })

    // generate scaled value for graph
    normalizedGroups.map(item => {
      item['scaled_value'] = wordCore.scaleBetween(item.count,
                                                   1,
                                                   100,
                                                   normalizedGroups[0].count,
                                                   normalizedGroups[normalizedGroups.length-1].count)
    })

    // total of all the words in the top 100
    var total = 0
    normalizedGroups.map(item =>{
      total += item.count
    })

    this.setState({
      current_data: normalizedGroups.reverse(),
      highValue: list[0].value,
      lowValue: list[list.length-1].value,
      totalValue: total,
      selected: event.target.dataset.id
    })
  }

  getWordNodes = () => {
    return (
      this.state.dataIds.map(id => {

        var data = this.state.data[id]

        return (
          <div key={data.id} data-id={data.id}
               className={`site-data-selector ${this.state.selected == data.id ? 'selected' : ''}`}
               onClick={ this.selectData }>
               {moment.unix(data.date_created).fromNow()}
         </div>
        )
      })
    )
  }

  getDataNodes = () => {
    return (
      this.state.current_data.map(item => {
        return (
          <div key={item.count} className="site-data-item-container">
            <div className="site-data-bar" style={{width: `${item.scaled_value}%`}}/>
            <div className="site-data-item">
              {`${item.count}`}
            </div>
          </div>
        )
      })
    )
  }

  render () {
    return (
      <div className="site-content">
        <div className="site-content-header">
          <h3>Fetched</h3>
        </div>
        <div className="history">
          { this.getWordNodes() }
        </div>
        <div className="site-content-actions">
          <button className="button" onClick={ this.refreshFetch }>Fetch</button>
        </div>
        <div className="site-data-stats">
          <div className="site-data-stat">Max {this.state.highValue}</div>
          <div className="site-data-stat">Min {this.state.lowValue}</div>
          <div className="site-data-stat">Total Words {this.state.totalValue}</div>
        </div>
        <div className="site-data">
          <div classname="scale">
            <div className="mid" />
          </div>
          {this.getDataNodes()}
        </div>
      </div>
    )
  }
};
