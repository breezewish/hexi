var _ = require('lodash');
var webpack = require('webpack');
var utils = require('./utils');

module.exports = function (env) {
  var resolve = require('./resolve')(env);
  return {
    entry: {
      app: resolve.workingRoot('ui/main.js'),
    },
    output: {
      path: resolve.workingRoot('.ui_built'),
      filename: 'main.js',
      publicPath: env.type === 'core'
        ? '/core/static/'
        : `/plugins/${env.pluginName}/static/`
        ,
    },
    resolve: {
      extensions: ['.js', '.vue'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
        '@module': resolve.workingRoot('ui'),
        '@core': resolve.coreRoot('ui'),
      },
    },
    module: {
      rules: _.concat(utils.styleLoaders(), [
        {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: utils.cssLoaders(),
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: [
            resolve.workingRoot('ui'),
            resolve.coreRoot('ui'),
          ],
        },
        {
          test: /\.plugin$/,
          loader: 'ini-loader',
        },
        {
          test: /\.(png|jpe?g|gif)(\?.*)?$/,
          loader: 'url-loader',
          options: {
            limit: 10000,
            name: 'img/[name].[hash:7].[ext]',
          }
        },
        { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
        { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
      ]),
    },
    plugins: [
      new webpack.LoaderOptionsPlugin({
        stylus: {
          default: {
            preferPathResolver: 'webpack',
            import: ['~@core/assets/import.styl'],
          },
        },
      }),
      new webpack.DllReferencePlugin({
        manifest: resolve.coreRoot('.ui_built/core_dll_manifest.json'),
      }),
    ],
  }
};
