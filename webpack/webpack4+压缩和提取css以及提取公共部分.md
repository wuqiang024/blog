## 提取: mini-css-extract-plugin
***
在过去，如何将css提取到一个文件中是`extract-text-webpack-plugin`的工作，不幸的是这个插件和webpack4不太兼容。
在webpack4+版本，我们可以使用mini-css-extract-plugin插件来解决这个问题。

首先进行安装
```js
npm install mini-css-extract-plugin -D
```

接下来我们需要在webpack的配置文件中引入
```js
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
```

然后在scss等样式相关的rules中使用它;
```js
{
    test: /\.(sa|sc|c)ss$/,
    use: [
        'css-hot-loader',
        MiniCssExtractPlugin,
        'css-loader',
        'sass-loader'
    ]
}
```

最后我们要在plugins中使用
```js
    new MiniCssExtractPlugin({
        filename: './css/[name].css' // 提取出来的css文件路径以及命名
    })
```

值得一提的是，最好将mini-css-extract-plugin用于生产模式，因为该插件使用目前会导致HMR功能缺失，因此在平常的开发模式中，我们还是使用style-loader。
保存之后运行npm run build，会发现打包后文件夹已经帮我们把css提取出来。

到这里我们会发现一个问题，结合之前的devtool和devServer以及现在的提取插件，我们会发现在开发模式和生产模式下，我们的webpack配置会有所不同，因此，我们大可将开发模式和生产模式的webpack配置分成两个文件来使用。例如`webpack.dev.js`和`webpack.prod.js`。

当然，如果对配置文件命名进行修改，我们需要对package.json文件中的build和dev命令进行修改，通过--config引导命令读取相应的配置文件:
```
"build": "webpack --progress --config ./config/webpack.prod.js",
"dev": "webpack-dev-server --open --hot --progress --config ./config/webpack.dev.js"
```

## 压缩: optimize-css-assets-webpack-plugin
***
optimize-css-assets-webpack-plugin用于压缩css文件，他将在webpack构建期间搜索css资源，并将优化/最小化css(默认情况下它使用cssnano,但可以指定自定义css处理器)
他解决了extract-text-webpack-plugin css重复问题: 由于extract-text-webpack-plugin仅捆绑(合并)文本块，如果它用于捆绑css，则捆绑包可能具有重复的条目

```js
new OptimizeCssAssertsPlugin({
    assetNameRegExp: /\.css$/g, // 一个正则表达式，指示应优化/最小化的资产的名称，提供的正则表达式针对配置中ExtractTextPlugin实例导出的文件的文件名运行，而不是源css
    cssProcessor: require('cssnano'), // 用于优化/最小化css的css处理器，默认为cssnano
    cssProcessorOptions: { safe: true, discardComments: { removeAll: true}}, // 传递给cssProcessor的配置选项，默认为{}
    canPrint: true // 一个布尔值，指示插件是否可以将消息打印到控制台，默认为true
})
```

保存，运行build命令，会发现打包后的css文件已经被压缩。

## 提取公共部分: optimization
***
当我们在编写多入口文件的项目时，难免在不同的入口文件会有相同的部分(比如说存在部分相同的样式，使用了相同的组件，使用了公共样式等)，因此，我们需要在打包过程中提取公共的部分并独立开来。
在之前版本的webpack中，我们可以使用CommonsChunkPlugin进行提取，而在webpack4+版本中，CommonsChunkPlugin已经从webpack4中移除，webpack4+版本使用内置的SplitChunksPlugin插件来进行公共部分的提取。

因为SplitChunksPlugin是webpack4+版本内置的插件，所以无需安装，只需在webpack.config.js中配置。

```js
    plugins: [...],
    optimization: {
        splitChunks: {
            cacheGroups: {
                commons: {
                    name: 'commons', // 给提取出来的文件命名
                    chunks: 'initial', // initial表示提取入口文件的公共部分
                    minChunks: 2, // 表示提取公共部分最少的文件数
                    minSize: 0 // 表示提取公共部分最小的大小
                }
            }
        }
    }
```
保存，使用插件之后运行build。

![https://img-blog.csdnimg.cn/20181220161153313.png](https://img-blog.csdnimg.cn/20181220161153313.png)

可以看到，webpack帮我们把js和css中公共的部分提取出来并放置到commons的文件中(如图中的commons.js和commons.css)。