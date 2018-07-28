var path = require('path');

module.exports = function (env) {

  const ret = {};

  ret.root = function (dir) {
    return path.join(__dirname, '../..', dir || '.');
  };

  ret.coreDirectory = ret.root('hexi');

  if (env.type === 'core' || env.type === 'coreDll') {
    ret.workingDirectory = ret.coreDirectory;
  } else {
    ret.workingDirectory = ret.root(`plugins/${env.pluginName}`);
  }

  ret.coreRoot = function (dir) {
    return path.join(ret.coreDirectory, dir || '.');
  };

  ret.workingRoot = function (dir) {
    return path.join(ret.workingDirectory, dir || '.');
  };

  return ret;

};
