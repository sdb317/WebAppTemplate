var path = require("path");
var webpackConfig = require("./webpack.config");

var target = "tests";

module.exports = Object.assign({}, webpackConfig, {
  entry: [
    "babel-polyfill",
    "./app/js/" + target // The is the entry point. The extensions will be specified later in the `resolve` section.
  ],

  output: {
    path: __dirname,
    filename: "app/js/" + target + ".bundle.js" // This is where the compiled bundle will be stored.
  },

  devtool: "source-map",

  devServer: {
    contentBase: path.resolve("."),
    inline: true,
    historyApiFallback: {
      index: "tests.html"
    },
    proxy: {
      "/templates/": {
        target: "http://localhost:8000",
        // target: 'https://localhost:8000', // If using SSL
        secure: false
      },
      "/api/v1/": {
        target: "http://localhost:8000",
        // target: 'https://localhost:8000', // If using SSL
        secure: false
      }
    }
    // hot: true
  }
});

// .\node_modules\.bin\webpack-dev-server --config webpack.config.tests.js
