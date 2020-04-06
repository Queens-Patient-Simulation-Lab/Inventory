var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  context: __dirname,

  mode: 'development',
  devtool: "source-map",

  entry: {
    "main": './assets/js/index',
    "chrome": './assets/scss/chrome',
    "login": './assets/scss/login',
    "item_details": ['./assets/scss/item_details', './assets/js/item_details'],
    "homepage": "./assets/js/homepage",
    "locations": "./assets/js/locations"
  },

  output: {
    path: path.resolve('./assets/bundles/'),
    filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({ filename: './webpack-stats.json' }),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
    }),
  ],

  module: {
    rules: [
      {
        test: /\.(scss)$/,
        use: [MiniCssExtractPlugin.loader, {
          loader: 'css-loader', // translates CSS into CommonJS modules
        }, {
          loader: 'postcss-loader', // Run postcss actions
          options: {
            plugins: function () { // postcss plugins, can be exported to postcss.config.js
              return [
                require('autoprefixer')
              ];
            }
          }
        }, {
          loader: 'sass-loader' // compiles Sass to CSS
        }]
      }
    ]
  },

  resolve: {
    extensions: ['.js', '.scss']
  },
}

