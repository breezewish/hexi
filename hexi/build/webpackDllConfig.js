var webpack = require('webpack');

module.exports = function (env) {
  var resolve = require('./resolve')(env);
  return {
    output: {
      publicPath: '/core/static/',
    },
    entry: {
      dll: [
        'axios',
        'element-ui',
        'lodash',
        'vue',
        'vuex',
        'vue-moment',
        'vue-router',
        'vue-chartjs',
        'babel-runtime/helpers/asyncToGenerator.js',
        'babel-runtime/regenerator/index.js',
      ],
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
      },
    },
    module: {
      rules: [
        { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
        { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" }
      ],
    },
    output: {
      path: resolve.coreRoot('.ui_built'),
      filename: 'core_dll.js',
      library: 'hexiCoreDll',
    },
    plugins: [
      new webpack.DllPlugin({
        path: resolve.coreRoot('.ui_built/core_dll_manifest.json'),
        name: 'hexiCoreDll',
      }),
    ],
  };
}
