const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const root = (p = '.') => path.resolve(__dirname, p);

const config = {
  entry: {
    app: root('./src/application.js'),
  },
  output: {
    path: root('./dist'),
    filename: '[name].js',
  },
  resolve: {
    modules: [
      root('./node_modules'),
    ],
    alias: {
      '@': root('./src'),
    },
  },
  target: 'web',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env'],
            plugins: ['transform-runtime'],
          },
        },
      },
      {
        test: /\.json$/,
        use: 'json-loader',
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: root('src/template.html'),
    }),
  ],
  devServer: {
    port: 5678,
  },
};

module.exports = config;
