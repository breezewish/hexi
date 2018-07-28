exports.cssLoaders = function () {
  function generateLoaders (loader) {
    const loaders = ['vue-style-loader', 'css-loader'];
    if (loader) {
      loaders.push(`${loader}-loader`);
    }
    return loaders;
  }
  return {
    css: generateLoaders(),
    postcss: generateLoaders(),
    stylus: generateLoaders('stylus'),
    styl: generateLoaders('stylus'),
  };
};

exports.styleLoaders = function () {
  var output = [];
  var loaders = exports.cssLoaders();
  for (var extension in loaders) {
    var loader = loaders[extension]
    output.push({
      test: new RegExp('\\.' + extension + '$'),
      use: loader
    });
  };
  return output;
};
