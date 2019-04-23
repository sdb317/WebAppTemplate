// Pull in dependencies
var path = require("path");
var webpack = require("webpack");

module.exports = {
  context: __dirname,

  module: {
    rules: [
      // A regexp that tells webpack use the following loaders on all .js and .jsx files
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },

  externals:{
    "LOG_LEVEL": '"debug"'
  },

  plugins: [
    new webpack.ProvidePlugin({ // Makes jQuery available in every module
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    })
  ],

  resolve: {
    // Extensions that should be used to resolve modules
    extensions: [".js", ".jsx"]
  },

};