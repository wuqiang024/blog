# 带你深入理解webpack(进阶篇)
***
## 静态资源拷贝
***
有些时候，我们需要使用已有的JS文件,CSS文件(本地文件)，但是不需要webpack编译，例如，我们在`public/index.html`中引入了public目录下的js或css文件。这个时候，如果直接打包，那么在构建出来之后，肯定是找不到对应的`js/css`了。

```js
// public目录解构
|__public
|   |__config.js
|   |__index.html
|   |__js
|   |   |__base.js
|   |   |__other.js
|   |__login.html
```

现在，我们在index.html中引入了`./js/base.js`。

```js
// index.html
<script src="./js/base.js"></script>
```

这个时候我们`npm run dev`，会发现有找不到该资源文件的报错信息。

对于这个问题，我们可以手动将其拷贝至构建目录，然后在`CleanWebpackPlugin`时，注意不要清空对应的文件或文件夹即可，但是如果这个静态文件时不时还需要更改一下，那么依赖于手动拷贝，是很容易出问题的。

这时候可以用`CopyWebpackPlugin`，它的作用就是将单个文件或整个目录赋值到构建目录。

```js
npm install copy-webpack-plugin -D
```

修改配置，需要做的是将`public/js`目录拷贝至`dist/js`目录。

```js
const CopyWebpackPlugin = require('copy-webpack-plugin');
module.exports = {
    plugins: [
        new CopyWebpackPlugin([
            {
                from: 'public/js/*.js',
                to: path.resolve(__dirname, 'dist', 'js'),
                flatten: true
            },
            // 还可以继续配置其他要拷贝的文件
        ])
    ]
}
```

此时，重新执行npm run dev，报错信息已经消失。

这里说一下flatten参数，设置为true，那么它只会拷贝文件，而不会把文件夹路径都靠背上。

另外，如果我们需要拷贝一个目录下的很多文件，但是想过滤掉某个或某些文件，那么`CopyWebpackPlugin`还为我们提供了ignore参数。

```js
module.exports = {
    plugins: [
        new CopyWebpackPlugin([
            {
                from: 'public/js/*.js',
                to: path.resolve(__dirname, 'dist', 'js'),
                flatten: true
            },
        ], {
            ignore: ['other.js']
        })
    ]
}
```

这里，我们忽略掉js目录下的other.js文件，使用npm run build构建，可以看到dist/js下不会出现other.js文件。

## providePlugin
***
ProvidePlugin在我看来，是为懒人准备的，不过也别过度使用，毕竟全局变量不是什么好东西。ProvidePlugin的作用就是不需要import或require就可以在项目中到处使用。

`ProvidePlugin`是webpack的内置插件。使用方式如下:

```js
new webpack.ProvidePlugin({
    identifier1: 'module1',
    identifier2: ['module2', 'property2']
})
```

默认寻找路径是当前文件夹`./**`和`node_modules`，当然，你也可以指定全路径。

```js
const webpack = require('webpack');
module.exports = {
    new webpack.ProvidePlugin({
        React: 'react',
        Component: ['react', 'Component'],
        Vue: ['vue/dist/vue.esm.js', 'default'],
        $: 'jquery',
        _map: ['lodash', 'map']
    })
}
```

这样配置之后，你就可以在项目中随心所欲的使用$,_map了，并且写React组件时，也不需要import React和Component了，如果你想的话，还可以把React的Hooks都配置在这里。

另外呢，Vue的配置后面多了一个default，因为vue.esm.js中使用的是`export defalut`，对于这种，必须要指定`default`。
React使用的是module.exports导出的，因此不需要写default。

另外，如果你项目启动了eslint的话，记得修改eslint的配置文件，增加以下配置:

```js
{
    "globals": {
        "React": true,
        "Vue": true
    }
}
```

## 抽离css
***
`npm install mini-css-extract-plugin -D`。

> mini-css-extract-plugin和extract-text-webpack-plugin比较`

1、异步加载
2、不会重复编译(性能更好)
3、更容易使用
4、只适用css

修改我们的配置文件:

```js
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
module.exports = {
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/[name].css'
            // 个人习惯将css文件放在单独的目录下
            // publicPath: '../'  // 如果你的output的publicPath配置的是'./'这种相对路径，那么如果将css文件放在单独目录下，记得在这里指定一下publicPath
        })
    ],
    module: {
        rules: [
            {
                test: /\.(le|c)css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                    'sass-loader'
                ],
                exclude: /node_modules/
            }
        ]
    }
}
```

现在我们重新编译，目录结构变为以下所示:

```js
|__dist
|   |__assets
|       |__1.jpg
|   |__css
|       |__index.css
|       |__index.css.map
|   |__bundle.hash.js
|   |__bundle.hash.js.map
|   |__index.html
```

前面说了最好建一个.browserslistrc文件，这样可以多个loader共享配置，所以，动手在根目录下新建文件(.browserslistrc)，内容如下(你可以根据自己项目需求，修改为其他的设置)

```js
last 2 version
> 0.2%
not dead
```

## 将抽离出来的css进行压缩
***
使用`mini-css-extract-plugin`，css文件默认不会压缩,如果想要压缩，需要配置`optimization`，首先安装`optimize-css-assets-webpack-plugin`.

修改webpack配置:

```js
const OptimizeCssPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    plugins: [
        new OptimizeCssPlugin()
    ]
}
```

注意，这里将`OptimizeCssPlugin`直接配置在`plugins`里面，那么js和css都能正常压缩，如果你将这个配置在optimization，那么需要再配置一下js的压缩(开发环境下不需要去做css的压缩，因此后面记得将其放到`webpack.config.prod.js`里).

配置完后，测试的时候发现，抽离之后，修改css文件时，第一次页面会刷新，但是第二次页面不会再刷新。我们再次修改下对应的rule。

```js
module.exports = {
    rules: [
        {
            test: /\.(c|sa)ss$/,
            use: [
                {
                    loader: MiniCssExtractPlugin.loader,
                    options: {
                        hmr: isDev,
                        reloadAll: true
                    }
                }
            ],
            exclude: /node_modules/
        }
    ]
}
```

## 按需加载
***
很多时候我们不需要一次性加载所有的JS文件，而应该在不同阶段去加载所需要的代码，webpack内置了强大的分割代码的功能可以实现按需加载。

比如，我们在点击了某个按钮之后，才需要使用对应的JS文件中的代码，需要使用`import()`语法。

```js
document.getElementById('btn').onclick = function() {
    import('./handle').then(fn => fn.default())
}
```

`import()`语法，需要`@babel/plugin-syntax-dynamic-import`的插件支持，但是因为当前`@babel/preset-env`预设中已经包含了`@babel/plugin-syntax-dynamic-import`,因此我们不需要再单独安装和配置。

`webpack`遇到`import(****)`这样的语法的时候，会这样处理:
* 以****为入口新生成一个chunk
* 当代码执行到`import`所在的语句时，才会加载`chunk`所对应的文件(如这里的`1.bundle.[hash].js`)。

大家可以在浏览器的控制台中，在`network`的tab页查看文件加载的情况，只有点击之后，才会加载对应的js.

## 热更新
***
1、首先配置`devServer`的hot为true
2、并且在plugins中增加`new webpack.HotModuleReplacementPlugin()`。

```js
const webpack = require('webpack');

module.exports = {
    devServer: {
        hot: true
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin() // 热更新插件
    ]
}
```

我们配置了`HotModuleReplacementPlugin`之后，会发现，此时我们修改代码，仍然是整个页面都会刷新。不希望整个页面刷新，还需要修改入口文件。

3、在入口文件前新增

```js
if(module && module.hot) {
    module.hot.accept()
}
```

此时，再修改代码，不会造成整个页面的刷新。

## 多页面打包
***
有时，我们的应用不一定是一个单页应用，而是一个多页应用，那么如何使用`webpack`进行打包呢。为了生成目录看起来清晰，不生成单独的map文件。

```js
cosnt path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
        index: './src/index.js',
        login: './src/login.js',
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].[hash:6].js',
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html',
            filename: 'index.html',
        }),
        new HtmlWebpackPlugin({
            template: './public/login.html',
            filename: 'login.html'
        })
    ]
}
```

如果需要配置多个`HtmlWebpackPlugin`，那么filename字段不可缺省，否则默认生成的都是index.html，如果你希望html的文件名中也带有hash，那么直接修改filename字段即可，例如: `filename: 'login.[hash:6].html'`。

看起来是ok了，不过查看index.html和login.html都会发现，都同时引入了index.[hash].js和login.[hash].js。我们希望，index.html只引入index.js, login.html只引入login.js。

HtmlWebpackPlugin提供了一个`chunks`参数，可以接收一个数组，配置此参数仅会将数组中指定的js引入html文件，此外，如果你需要引入多个JS文件，仅有少数不想引入，还可以指定`excludeChunks`参数，它接受一个数组。

```js
module.exports = {
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html',
            filename: 'index.html',
            chunks: ['index']
        }),
        new HtmlWebpackPlugin({
            template: './public/login.html',
            filename: 'login.html',
            chunks: ['login']
        })
    ]
}
```

## resolve配置
***
`resolve`配置`webpack`如何寻找模块所对应的文件。`webpack`内置`JavaScript`模块化语法解析功能，默认会采用模块化标准里约定好的规则去寻找，但你可以根据自己的需要修改默认的规则。

`1、modules`
`resolve.modules`配置webpack去哪些目录下寻找第三方模块，默认情况下，只会去`node_modules`下寻找，如果你我项目中某个文件夹下的模块经常被导入，不希望写很长的路径，那么就可以通过配置`resolve.modules`来简化。

```js
module.exports = {
    resolve: {
        modules: ['./src/components', 'node_modules'] // 从左到右依次查找
    }
}
```

这样配置以后，我们`import Dialog from 'dialog'`，会去寻找`./src/components/dialog`，不再需要使用相对路径导入。如果在`./src/components`下找不到的话，就会到`node_modules`下寻找。

`2、alias`
`resolve.alias`配置项通过别名把原导入路径映射成一个新的导入路径，例如:

```js
module.exports = {
    resolve: {
        alias: {
            'react-native': '@my/react-native/web',
        }
    }
}
```

例如，我们有一个依赖`@my/react-native-web`可以实现`react-native`转`web`，我们代码一般这样:

```js
import { View, ListView, StyleSheet, Animated } fron 'react-native';
```

配置了别名后，在转web时，会从`@my/react-native-web`寻找对应的依赖。

`3、extensions`
适配多端的项目中，可能会出现`.web.js`,`.wx.js`，例如在转web的项目中，我们希望首先找`.web.js`，如果没有再找`.js`。我们可以这样配置:

```js
module.exports = {
    resolve: {
        extensions: ['.web.js', '.js'] // 还可以配置.json, .css
    }
}
```

首先寻找`../dialog.web.js`，如果不存在的话，再寻找`./dialog.js`。这在适配多端的代码中非常有用，否则你就需要根据不同的平台去引入文件(以牺牲了速度为代价)。

当然，在配置`extensions`时，我们就可以缺省文件后缀，在导入语句没带文件后缀时，会自动带上`extensions`中配置的后缀后，去尝试访问文件是否存在，因此要将高频的后缀放在前面，并且数组不要太长，减少尝试次数。如果没有配置`extensions`，默认只会找对应的js文件。

`4、enforceExtension`
如果配置了`resolve.enforceExtension`为`true`，那么导入语句不能缺省文件后缀。

`5、mainFields`
有一些第三方模块会提供多份代码，例如`bootstrap`，可以查看`bootstrap`的`package.json`文件。

```js
{
    "style": "dist/css/bootstrap.css",
    "sass": 'scss/bootstrap.scss",
    "main": "dist/js/bootstrap"
}
```

`resolve.mainFields`默认配置是`['browser', 'main']`，即首先找对应依赖`package.json`中的`browser`字段，如果没有，找`main`字段。

如:`import 'bootstrap'`默认情况下，找的是对应依赖的`package.json`的`main`字段指定的文件，即`dist/js/bootstrap`。

假设我们希望,`import 'bootstrap'`默认去找`css`文件的话，可以配置`resolve.mainFields`为:

```js
module.exports = {
    resolve: {
        mainFields: ['style', 'main']
    }
}
```

## 区分不同的环境
***
目前为止我们webpack的配置，都定义在了`webpack.config.js`中，对于需要区分是开发环境还是生产环境的情况，我们根据`process.env.NODE_ENV`去做了区分配置，但是配置文件中如果有多处需要区分环境的配置，这显然不是一个好办法。

更好的做法是创建多个配置文件，如`webpack.base.js`,`webpack.dev.js`,`webpack.prod.js`。

* `webpack.base.js` 定义公共配置
* `webpack.dev.js` 定义开发环境的配置
* `webpack.prod.js` 定义生产环境的配置

`webpack-merge`专为`webpack`设计，提供了一个`merge`函数，用于连接数组，合并对象。

`npm install webpack-merge -D`

```js
const merge = require('webpack-merge');
merge({
    devtool: 'cheap-module-eval-source-map',
    module: {
        rules: [
            {a: 1}
        ]
    },
    plugins: [1, 2, 3]
}, {
    devtool: 'none',
    mode: 'production',
    module: {
        rules: [
            {a: 2},
            {b: 1}
        ]
    },
    plugins: [4, 5, 6]
});

// 合并后为
{
    devtool: 'none',
    mode: 'production',
    module: {
        rules: [
            {a: 1},
            {a: 2},
            {b: 1}
        ]
    },
    plugins: [1, 2, 3, 4, 5, 6]
}
```

`webpack.config.base.js`中是通用的`webpack`配置，以`webpack.config.dev.js`为例，如下:

```js
const merge = require('webpack-merge');
const baseWebpackConfig = require('./webpack.config.base');

module.exports = merge(baseWebpackConfig, {
    mode: 'development',
    // 其他配置
});
```

然后修改我们的package.json，指定对应的`config`文件:

```js
{
    "scripts": {
        "dev": "cross-env NODE_ENV=development webpack-dev-server --config=webpack.config.dev.js",
        "build": "cross-env NODE_ENV=production webpack --config=webpack.config.prod.js"
    }
}
```

你可以使用`merge`合并，也可以使用`merge.smart`合并，`merge.smart`在合并`loader`时，会将同一匹配规则的进行合并。

## 定义环境变量
***
很多时候，我们会在开发环境中使用预发环境或者是本地的域名，生产环境使用线上域名，我们可以在webpack定义环境变量，然后在代码中使用。

使用`webpack`内置插件`DefinePlugin`来定义环境变量。

`DefinePlugin`中的每个键，是一个标识符。

* 如果`value`是一个字符串，会被当做`code`片段
* 如果`value`不是一个字符串，会被`stringify`
* 如果`value`是一个对象，正常对象定义即可
* 如果`key`中有`typeof`，它只针对`typeof`调用定义

```js
const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            DEV: JSON.stringify('dev'), // 字符串
            FLAG: 'true' // FLAG 是个布尔值
        })
    ]
}
```

```js
// index.js
if(DEV === 'dev') {
    // 开发环境
} else {
    // 生产环境
}
```

## 利用webpack解决跨域问题
***
假设前端在3000端口，服务端在4000端口，我们通过webpack配置的方式去解决跨域。

首先，我们在本地创建一个`server.js`

```js
let express = require('express');
let app = express();

app.get('/api/user/', (req, res) => {
    res.json({name: '刘小溪'});
});

app.listen(4000);
```

执行代码，我们可以在浏览器访问到此接口: `http://localhost:4000/api/user`。

在`index.js`中请求`/api/user`，修改`index.js`如下:

```js
fetch('/api/user')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(err => console.log(err));
```

我们希望通过配置代理的方式，去访问4000的接口。

`配置代理`
修改webpack配置:

```js
module.exports = {
    devServer: {
        proxy: {
            '/api': 'http://localhost:4000'
        }
    }
}
```

重新执行`npm run dev`，可以看到控制台打印出来了结果`{name: "刘小溪"}`，实现了跨域。

大多情况，后端提供的接口并不包含`/api`，即:`/user`等，配置代理时，我们不可能罗列出每个api。

修改代理配置和服务端代码：

```js
let express = require('express');
let app = express();

app.get('/user', (req, res) => {
    res.json({name: '刘小溪'});
})

app.listen(4000);
```

```js
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:4000',
                pathRewrite: {
                    '/api': ''
                }
            }
        }
    }
}
```

## 前端模拟数据
***
> 简单模拟数据

```js
module.exports = {
    devServer: {
        before(app) {
            app.get(;'/user', (req, res) => {
                res.json({name: '刘小溪'})
            })
        }
    }
}
```

在index.js中直接请求`/user`接口。

```js
fetch('user')
    .then(response => reponse.json())
    .then(data => console.log(data))
    .then(err => console.log(err))
```

> 使用mocker-api mock数据接口
mocker-api为 REST API创建模拟API,在没有实际REST API服务器的情况下测试应用程序时，它会很有用。

`npm install mocker-api -D`

在项目中新建mock文件夹，新建mocker.js文件，文件如下:

```js
module.exports = {
    'GET /user': {name: '刘小溪'},
    'POST /login/account': (req, res) => {
        const { password, username } = req.body;
        if(password === '888888' && username === 'admin') {
            return res.send({
                status: 'ok',
                code: 0,
                token: 'sdsdsdsd',
                data: {id: 1, name: '刘小溪'}
            })
        }
    }
}
```

修改`webpack.config.base.js`。

```js
const apiMocker = require('mocker-api');
module.exports = {
    devServer: {
        before(app) {
            apiMocker(app, path.resolve('./mock/mocker.js'))
        }
    }
}
```