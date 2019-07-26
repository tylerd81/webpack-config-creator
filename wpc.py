from os import path

use_sass = False
use_file_loader = False
use_html_plugin = False

# check if a webpack.config.js already exists
if path.exists("webpack.config.js"):
  print("There is already an existing webpack.config.js in this directory!")
  exit()


print(
  """
  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  wpc defaults to src/index.js as the input and dist/bundle.js as the output.
  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  """)

sass_input = input("Do you want to use SASS? [Y/N] ")

if sass_input.lower() == "y":
  use_sass = True

loader_input = input("Use file-loader (for images)? [Y/N] ")
if loader_input.lower() == "y":
  use_file_loader = True

loader_input = input("Use html-webpack-plugin for generating html? [Y/N] ")
if loader_input.lower() == "y":
  use_html_plugin = True
  divider = "*" * 65
  print("\n" + divider)
  print("wpc defaults to writing index.html and uses a template\nin src/pages/index.html when using html-webpack-plugin")
  print(divider + "\n")

webpack_config = "const path = require('path');\n"

if use_html_plugin:
  webpack_config += "const HtmlPlugin = require('html-webpack-plugin');\n"

webpack_config += """
module.exports = {
  entry: {
    main: './src/index.js'
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
"""

if use_sass:
  webpack_config +=  """
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader']
      },  
  """
webpack_config += """
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
"""

if use_html_plugin:
  webpack_config += """
      {
        test: /\.html$/,
        use: ['html-loader']
      },
  """

if use_file_loader:
  webpack_config += """
      {
        test: /\.(jpg|png)$/,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'images'
          }
        }
      },
  """

webpack_config += """
    ]
  },
  """
if use_html_plugin:
  webpack_config += """
  plugins: [
    new HtmlPlugin({
      filename: 'index.html',
      template: './src/pages/index.html',
      chunks: ['main']
    })
  ]
  """

webpack_config += "};\n"

npm_packages = "style-loader css-loader "
if use_file_loader:
  npm_packages += "file-loader "

if use_html_plugin:
  npm_packages += "html-loader html-webpack-plugin "

if use_sass:
  npm_packages += "sass-loader "

print("Don't forget to npm install " + npm_packages)

webpack_config_file = open("./webpack.config.js", "w")
webpack_config_file.write(webpack_config)
print("Your config file has been created!")

