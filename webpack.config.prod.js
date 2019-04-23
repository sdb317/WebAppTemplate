const webpackConfig = require("./webpack.config");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");

var target = "index";

module.exports = Object.assign({}, webpackConfig, {
  entry: [
    "./app/js/" + target // The is the entry point. The extensions will be specified later in the `resolve` section.
  ],

  output: {
    path: __dirname,
    filename: "app/static/app/js/" + target + ".bundle.js" // This is where the compiled bundle will be stored.
  },

  externals:{
    "LOG_LEVEL": '"prod"'
  },

  plugins: [
    new UglifyJsPlugin()
  ]
});

// .\node_modules\.bin\webpack -p --config webpack.config.prod.js
