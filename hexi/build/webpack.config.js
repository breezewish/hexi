var webpack = require('webpack');
var path = require('path');
var fs = require('fs');
var utils = require('./utils');

function root(dir) {
  return path.join(__dirname, '../..', dir || '.');
}

module.exports = function (env) {
  if (env.type === 'plugin') {
    if (!env.pluginName) {
      throw new Error('Please specify a plugin name. Sample: npm run build:plugin -- --env.pluginName PLUGIN_NAME');
    }
  } else if (env.type !== 'core' && env.type !== 'coreDll') {
    throw new Error('Unknown build target');
  }

  var resolve = require('./resolve')(env);

  var stat = fs.statSync(resolve.workingDirectory);
  if (!stat.isDirectory()) {
    throw new Error(`Expecting ${resolve.workingDirectory} to be a directory`);
  }

  if (!fs.statSync(`${resolve.workingDirectory}/ui`).isDirectory()) {
    throw new Error(`Expecting ${resolve.workingDirectory}/ui to be a directory`);
  }

  if (env.type === 'core') {
    return require('./webpackBaseConfig')(env);
  } else if (env.type === 'coreDll') {
    return require('./webpackDllConfig')(env);
  } else if (env.type === 'plugin') {
    return require('./webpackBaseConfig')(env);
  }

};

