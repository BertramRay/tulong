const path = require('path');
const webpack = require('webpack');
const { merge } = require('webpack-merge');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const baseWebpackConfig = require('./webpack.base.config.js');
const { VueLoaderPlugin } = require('vue-loader');
module.exports = merge(baseWebpackConfig, {
  mode: 'development',
  devServer: {
    port: 9003,
    hot: true,
    // https: true,
    // allowedHosts: 'all',
    historyApiFallback: {
      rewrites: [
        {
          from: /.*/,
          to: '/index.html'
        }
      ]
    },
  },
  plugins: [
    new VueLoaderPlugin(),
    new webpack.DefinePlugin({
      'NODE_ENV': JSON.stringify('development')
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',

    }),
    new HtmlWebpackPlugin({
      title: 'Tulong',
      filename: 'index.html',
      template: 'src/index.html',
    }),
  ]
})
