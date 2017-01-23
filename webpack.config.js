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
  resolve: {
    alias: {
      'react': path.join(__dirname, 'node_modules', 'react')
    }
  },
  module : {
    loaders : [
      {
        test : /\.jsx?/,
        exclude: /(node_modules|bower_components)|bundle.js|bundle.js.maps/,
        query: {
                plugins: [
                  'transform-runtime',
                  "transform-decorators-legacy",
                  'transform-class-properties'],
                presets: ['es2015','react', 'stage-3']
              },
        include : BUILD_DIR,
        loader : 'babel-loader'
      },
      { test: /\.css$/, loader: "style-loader!css-loader" },
      { test: /\.json$/, loader: "json-loader" }
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
