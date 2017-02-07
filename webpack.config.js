var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'app/static/public/js');
var STYLE_DIR = path.resolve(__dirname, 'app/static/public/css');
var APP_DIR = path.resolve(__dirname, 'app/static/public/js/components');

module.exports = {
  entry: ['babel-polyfill', APP_DIR + '/AppWrap.jsx'],
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  module : {
    loaders : [
      {
        test : /\.jsx?/,
        exclude: /(node_modules|bower_components)|bundle.js|bundle.js.maps/,
        include : BUILD_DIR,
        loader : 'babel-loader'
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': '"production"'
      }
    })
  ],
  watchOptions: {
    poll: true
  }
};
