var path = require('path');
var webpack = require('webpack');

module.exports = {
   entry: './static/src/index.js',
   output: {
       path: path.resolve(__dirname, 'static', 'build'),
       filename: 'bundle.js'
   },
   module: {
       loaders: [
           {
               loader: 'babel-loader',
               query: {
                   presets: ['es2015', 'react']
               }
           }
       ]
   },
   stats: {
       colors: true
   },
   devtool: 'source-map'
 };