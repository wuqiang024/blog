# 带你深度解锁webpack系列(基础篇)
***
## webpack是什么?
***
webpack是一个现代javascript应用程序的静态模块打包器，当webpack处理应用程序时，会递归构建一个依赖关系图，其中包含应用模块需要的每个模块，然后将这些模块打包成一个或多个bundle。

## webpack核心概念
***
* entry: 入口
* outpu: 输出
* loader: 模块转换器，用于把模块原内容按照需求转换成新内容
* 插件(plugins): 扩展插件，在webpack构建流程中的特定时机注入扩展逻辑来改变构建结果或做你想要做的事情。

## 初始化项目
***
新建一个文件夹，进入文件夹后执行`npm init -y`进行初始化。
要使用webpack就必须安装webpack,webpack-cli。
`npm install webpack webpack-cli -D`

鉴于前端技术变更迅速，祭出本篇文章基于webpack的版本号。

```js
|__ webpack@4.41.5
|__ webpack-cli@3.3.10
```

从webpack4.0开始，webpack是开箱即用的，在不引入任何配置文件的情况下就可以使用。

新建`src/index.js`文件。

```js
class Animal {
    constructor(name) {
        this.name = name;
    }
    getName() {
        return this.name
    }
}
const dog = new Animal('dog');
```

使用`npx webpack --mode=development`进行构建，默认是`production`模式，我们为了更清楚的查看打包后的代码，使用development模式。

可以看到项目下多了一个dist目录，里面有一个打包出来的文件main.js。

webpack有一个默认的配置，如默认的入口文件时`./src`，默认打包到`dist/main.js`。更多的默认配置可以查看:`node_modules/webpack/lib/WebpackOptionsDefaulter.js`。

查看`dist/main.js`文件，可以看到，`src/index.js`并没有被转译成低版本的代码，这显然不是我们想要的。

## 将js转译成低版本
***
前面我们说了webpack的四个核心概念，其中之一就是loader，loader用于对源代码进行转换，这正是我们现在所需要的。

将JS代码向低版本转换，我们需要使用`babel-loader`。
`npm install babel-loader -D`

此外，我们还需要配置babel，为此我们需要安装以下依赖:

```js
npm install @babel/core @babel/preset-env @babel-plugin-transform-runtime -D
npm install @babel/runtime @babel/runtime-corejs3
```

新建webpack.config.js，如下:

```js
module.exports = {
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: ['babel-loader'],
                exclude: /node_modules/,  // 排除node_modules目录
            }
        ]
    }
}
```

建议给loader指定`include`或`exclude`，指定其中一个即可，因为`node_modules`目录通常不需要我们去编译，排除后，有助于提升编译效率。

这里，我们可以在.babelrc中编写babel的配置，也可以在webpack.config.js中进行配置。

创建一个.babelrc:
配置如下:

```js
{
    "presets": ["@babel/preset-env"],
    "plugins": [
        [
            "@babel/plugin-transform-runtime",
            {
                "corejs": 3
            }
        ]
    ]
}
```

现在，我们重新执行`npx webpack --mode=develepment`，查看dist/main.js，会发现已经被编译成了低版本的js代码。

在webpack.config.js中配置:

```js
module.exports = {
    rules: [
        {
            test: /\.jsx?$/,
            use: ['babel-loader'],
            options: {
                presets: ['@babel/preset-env'],
                plugins: [
                    [
                        '@babel/plugin-transform-runtime',
                        {
                            'corejs': 3
                        }
                    ]
                ]
            },
            exclude: /node_modules/
        }
    ]
}
```

这里有几点需要说明:
* loader需要配置在module.rules中，rules是一个数组。
* loader的格式为:

```js
{
    test: /\.jsx?$/, // 匹配规则
    use: 'babel-loader'
}
```

或者也可以像这样:

```js
// 适用于只有一个Loader的情况
{
    test: /\.jsx?/,
    loader: 'babel-loader',
    options: {}
}
```

test字段是匹配规则，针对符合规则的文件进行处理。
use字段有几种写法:
* 可以是一个字符串
* 可以是一个数组
* use数组的每一项既可以是字符串也可以是一个对象，当我们需要在webpack的配置文件中对loader进行配置，就需要将其编写为一个对象，并且在此对象的options字段中进行配置。如:

```js
rules: [
    {
        test: /\.jsx?/,
        use: {
            loader: 'babel-loader',
            options: {
                presets: ["@babel/preset/env"]
            }
        },
        exclude: /node_modules/
    }
]
```

## mode
***
将mode增加到webpack.config.js中

```js
module.exports = {
    mode: 'development'
}
```
mode配置项，告知webpack使用相应模式的内置优化。
mode的配置项，支持以下两个配置。
* development: 将process.env.NODE_ENV设置为development，启用NamedChunksPlugin和NamedModulesPlugin
* production: 将process.env.NODE_ENV的值设置为production，启用FlagDependencyUsagePlugin,FlagIncludedChunksPlugin,ModuleConcatenationPlugin,NoEmitOnErrorsPlugin,OccurrenceOrderPlugin,SideEffectsFlagPlugin和UglifyJsPlugin

现在，我们直接使用npx webpack进行编译即可。

## 在浏览器中看页面
***
查看页面，难免就要用到html文件，有时候打包文件中带着hash，那么每次生成的文件名会有所不同，我们可以使用html-webpack-plugin来帮助我们完成这些事情。
`npm install html-webpack-plugin -D`.

新建public目录，并在其中新建一个index.html，修改webpack.config.js文件。

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = {
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html', // 模板文件名
            filename: 'index.html', // 打包后的文件名
            minify: {
                removeAttributeQuotes: false, // 是否删除属性的双引号
                collapseWhiteSpace: false, // 是否折叠空白
            },
            hash: true, // 是否加上hash，默认是false
        })
    ]
}
```

此时执行`npx webpack`可以看到dist目录下新增了index.html，并且其中自动插入了`<script>`脚本，引入的是我们打包之后的js文件。

这里要多说一点东西，HtmlWebpackPlugin为我们提供了一个`config`的配置，这个配置可以说是非常有用了。

`html-webpack-plugin`的config的妙用。
有时候，我们脚手架不仅仅是给自己使用，也许还提供给他人使用，Html文件的可配置性可能很重要，比如，你公司有专门的部分提供M页的公共头部/公共尾部，埋点jssdk以及分享的jssdk等，但是不是每个业务都需要这些内容。

一个功能可能对应多个js或css文件，如果每次都是业务自行修改public/index.html文件，也挺麻烦的，首先他们得搞清每个功能所需要引入的文件，然后才能对index.html进行修改。

此时我们增加一个配置文件，业务通过设置true或false来选出自己所需的功能，我们再根据配置文件的内容，为每个业务生成相应的html文件。

首先，我们在public目录下新增一个config.js(文件名可以随便自己取)，将其内容设置为:

```js
// public/config.js 除了以下配置外，这里面还可以有许多其他配置，例如,publicPath的路径等。
module.exports = {
    dev: {
        template: {
            title: '你好',
            header: false,
            footer: false
        }
    },
    build: {
        template: {
            title: '你好才怪',
            header: true,
            footer: false
        }
    }
}
```

现在，我们修改下我们的webpack.config.js。

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');
const isDev = process.env.NODE_ENV === 'development';
const config = require('./public/config')[isDev ? 'dev' : 'build'];

module.exports = {
    mode: isDev ? 'development' : 'production',
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html',
            filename: 'index.html',
            config: config.template
        })
    ]
}
```

相应的，我们需要修改我们的public/index.html文件(嵌入的js和css并不存在，仅作为示意):

```html
<html>
<head>
<% if(htmlWebpackPlugin.options.config.header) { %>
<link rel="stylesheet" type="text/css" href="common.css">
<% } %>
<title><%= (htmlWebpackPlugin.options.config.title) %></title>
</head>
<body>
<% if(htmlWebpackPlugin.options.config.header) { %>
<script src="common.js"></script>
<% } %>
```

`process.env`中默认并没有`NODE_ENV`,这里配置下我们的package.json中的scripts。为了兼容Window和Mac，我们先安装一下cross-env: `npm install cross-env -D`。

```js
// package.json
{
    "scripts": {
        "dev": "cross-env NODE_ENV=development webpack",
        "build": "cross-env NODE_ENV=production webpack"
    }
}
```

然后我们运行`npm run dev`和运行`npm run build`，对此下`dist/index.html`，可以看到生成的index.html中引入了对应的css和js，并且对应的title内容也不一样。

## 如何在浏览器中实时展示效果
***
安装`webpack-dev-server`。 `cnpm install webpack-dev-server -D`

修改package.json中的`scripts`:

```js
"scripts": {
    "dev": "cross-env NODE_ENV=development webpack-dev-server",
    "build": "cross-env NODE_ENV=production webpack"
}
```
在控制台执行`npm run dev`，启动正常，页面上啥也没有，修改下我们的JS代码，往页面中增加点内容，正常刷新(也就是说不需要任何配置就可以使用了)。

在配置了`html-webpack-plugin`的情况下，`contentBase`不会起任何作用。

```js
module.exports = {
    devServer: {
        port: '3000',  // 默认8080
        quite: false, // 默认不启用
        inline: true,  // 默认开启inline模式，如果设置为false，开启iframe模式
        stats: "errors-only", // 终端打印仅打印error
        clientLogLever: 'silent', // 日志等级
        compress: true, // 是否启用gzip压缩
    }
}
```

* 启用quiet后，除了初始启动信息之外的任何内容都不会打印到输出台，这也意味着来自webpack的错误或警告在控制台不可见。
* stats: "errors-only"，终端仅打印出error，注意当启用了quiet或noInfo时，此属性不起作用。---这个属性很有用，尤其是启用了eslint或者使用TS进行开发的时候，太多的编译信息在终端中，会干扰到我们。
* 启用overlay后，当编译出错时，会在浏览器窗口全屏输出错误，默认是关闭的。
* clientLogLevel: 当使用内联模式时，在浏览器的控制台将显示消息，如: 在重启之前，在一个错误之前，或者模块热替换启用。如果你不喜欢看到这些消息，可以将其设置为silent(none即将被移除)

## devtool
***
devtool中的一些设置，可以帮助我们将编译后的代码映射回原始源代码，不同的值会明显影响到构建和重新构建的速度。
对我们而言，能够定位到源码的行即可，因此，总和构建速度，在开发模式下，设置devtool的值时`cheap-module-eval-source-map`。

生产环境可以使用none或`source-map`，使用`source-map`最终会单独打印出一个`.map`文件，我们可以根据报错信息和此map文件，进行错误分析，定位到源代码。

`source-map`和`hidden-source-map`都会打包生成一个.map文件，区别在于,`source-map`会在打包出的js文件中增加一个引用注释，以便开发工具知道在哪里可以找到他。`hidden-source-map`则不会再打包的js中增加引用注释。

但是我们一般不会直接将.map文件部署到CDN，因为会直接映射到源码，更希望将.map文件传到错误解析系统，然后根据上报的错误信息，直接解析出出错的源码位置。

## 如何处理样式文件
***
webpack不能直接处理css，需要借助loader,如果是`.css`，我们需要的loader有: style-loader,css-loader，考虑到兼容性问题，还需要postcss-loader,而如果是less或sass，还需要less-loader或sass-loader。

```js
npm install style-loader css-loader postcss-loader autoprefixer sass-loader node-sass -D
```

```js
module.exports = {
    rules: [
        {
            test: /\.(sc|sa|c)ss$/,
            use: [
                'style-loader',
                'css-loader',
                {
                    loader: 'postcss-loader',
                    options: {
                        plugins: function() {
                            return [
                                require('autoprefixer')({
                                    "overrideBrowserslist": [
                                        ">0.25%",
                                        "not dead"
                                    ]
                                })
                            ]
                        }
                    }
                },
                'sass-loader'
            ],
            exclude: /node_modules/
        }
    ]
}
```

* style-loader 动态创建style标签，将css插入head中
* css-loader 负责处理@import语句
* postcss-loader和autoprefixer，自动生成浏览器兼容前缀
* sass-loader 负责处理编译.sass文件，将其转为css

这里，我们直接在webpack.config.js写了autoprefixer需要兼容的浏览器，仅仅为了方便展示，推荐大家在根目录下创建.browserslistrc，将对应规则写在此文件中，处理autoprefixer使用外，`@babel/preset-env`,`stylelint`,`eslint-plugin-compat`等都可以共有。

注意:
loader的执行顺序是从右往左执行的，也就是后面的loader先执行，上面loader 执行顺序为: sass-loader -> postcss-loader > css-loader > style-loader。
当然,loader还有一个参数，可以修改优先级， `enforce`参数，其值可以为:`pre(优先执行)`或`post(滞后执行)`。

现在一切看起来完美，但是假设我们的文件中使用了本地图片，例如:

```js
body {
    background: url('../images/other.png');
}
```

你就会发现，报错了。

## 图片/字体文件处理
***
我们可以使用`url-loader`或`file-loader`来处理本地的文件，`url-loader`和`file-loader`的功能类似，但是`url-loader`可以指定在文件大小小于指定的限制时，返回DataURL,因此，个人会优先选择使用`url-loader`。

```js
cnpm install url-loader -D
```

安装`url-loader`的时候，控制台会提示你，还需要安装`file-loader`，继续安装`file-loader`即可(新版npm不会自动安装peerDependencies)。

```js
module.exports = {
    modules: {
        rules: [
            {
                test: /\.(png|jpg|jpeg|gif|webp|svg|eot|ttf|woff|woff2)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 10240, // 10k
                            esModule: false
                        }
                    }
                ],
                exclude: /node_modules/
            }
        ]
    }
}
```

此处设置limit的值大小为10240，即资源大小小于10K时，将资源转为base64，超过10k，将图片拷贝到dist目录。esModule设置为false，否则，<img src={require('xxx.jpg')} /> 会出现<img src=[Module Object]/>，将资源转为base64可以减少网络请求次数，但是base64数据较大，如果太多的资源时base64，会导致加载变慢，因此设置limit值时，需要两者兼顾。

默认情况下，生成的文件的文件名就是文件内容的MD5哈希值并会保留所引用资源的原始扩展名，例如上面图片生成的文件名就如下:
```js
<style>
    body {
        background: url(afef7c0778d0edbd.jpg);
    }
</style>
```

当然你也可以通过参数修改:

```js
use: [
    {
        loader: 'url-loader',
        options: {
            limit: 10240,
            esModule: false,
            name: '[name]_[hash:6]:[ext]'
        }
    }
]
```

重新编译，在浏览器中审查元素，可以看到图片名变成了: thor_a5f7c0.jpeg。

当本地资源较多时，我们有时候会希望他们能打包在衣蛾文件夹下面，这也很简单，我们只需要在`url-loader`的options中指定outpath，如:`outPath:'assets'`，构建出的目录如下:

```js
|__dist
    |__assets
        |__ thor_afec.jpg
    |__index.html
    |__main.js
```

此时，如果你在`public/index.html`文件中，使用本地的图片，例如，我们修改一下`public/index.html`:
```js
<img src="./a.jpg">
```

重启本地服务，虽然控制台不会报错，但是你会发现，浏览器中根本加载不出这张图片，因为构建之后，通过相对路径根本找不到这张图片。

## 处理html中的本地图片
***
安装`html-withing-loader`来解决。`npm install html-withing-loader -D`

修改`webpack.config.js`:

```js
module.exports = {
    rules: [
        {
            test: /\.html$/,
            use: 'html-withing-loader'
        }
    ]
}
```

然后我们在我们的html中引入一张文件侧试一下.

```js
<!-- index.html -->
<img src="./thor.jpg">
```

重启本地服务，图片并没有加载，审查图片地址，发现图片的地址显示是`{"default":"assets/thor_a5f7.jpg"}`。

我当前的`file-loader`版本是5.0.2，5版本以后，需要增加`esModule`属性。

```js
module.exports = {
    modules: {
        rules: [
            {
                test: /\.(png|jpg|jpeg|svg|webp|eot|ttf|woff|woff2)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 10240,
                            esModule: false
                        }
                    }
                ]
            }
        ]
    }
}
```

再重启服务，就搞定了。
话说使用`html-withing-loader`处理图片后,html就不能使用vm,ejs的模板了，如果想继续在html中使用`<% if(htmlWebpackPlugin.options.config.header) { %>`这样的语句，但是又想能使用本地图片，可不可以，那就需要像下面一样编写图片的地址，并且删除`html-withing-loader`的配置即可。

```js
<img src="<%=require('./thor.jpg')%>" />
```

## 入口配置
***
入口字段为`entry`

```js
module.exports = {
    entry: './src/index.js'
}
```

entry的值可以是一个字符串，一个数组或一个对象。
字符串的情况无需多说，就是以对应的文件为入口。为数组时，表示有"多个主入口"，想要多个依赖文件一起注入时，会这样配置的。例如:

```js
entry: [
    './src/polyfill.js',
    './src/index.js'
]
```

polyfill.js文件中可能只是简单的引入了一些polyfill，例如babel-polyfill,whatwg-fetch等，需要在最前面被引入。

## 出口配置
***
配置output选项可以控制webpack如何输出编译文件。

```js
const path = require('path');
module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'), // 必须是绝对路径
        filename: 'bundle.js',
        publicPath: '/',  // 通常是CDN地址
    }
}
```

编译时，可以不配置，或者配置为'/',可以在我们之前提及的config.js中指定`publicPath`,当然还可以区分不同的环境指定配置文件来配置，或者根据isDev字段来设置。

除此以外，考虑到CDN缓存的问题，我们一般会给文件名加上hash。

```js
module.exports = {
    output: {
        path: path.resolve(__dirname, 'dist'), // 必须是绝对路径
        filename: 'bundle.[hash].js',
        publicPath: '/', // 通常是CDN地址
    }
}
```

如果你绝对hash串太长的话，还可以指定长度，例如`bundle.[hash:8].js`。

## 每次打包前清空dist目录
***
`npm install clean-webpack-plugin -D`。

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
module.exports = {
    plugins: [
        new CleanWebpackPlugin()
    ]   
}
```
`如果希望dist目录下某个文件夹不清空。`
有的时候，我们并不希望整个dist目录都被清空，比如，我们不希望，每次打包的时候，都删除dll目录，以及dll目录下的文件或子目录。
`clean-webpack-plugin`为我们提供了参数`cleanOnceBeforeBuildPatterns`。

```js
module.exports = {
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: ['**/*', '!dll', '!dll/**'], // 不删除dll目录下的文件 
        })
    ]
}
```

此外,`clean-webpack-plugin`还有一些其他配置。
