#起步阶段 使用webpack4.x构建vue的开发环境
***

## 安装依赖
***
```js
// 1、创建开发目录
mkdir webpack-vue && cd webpack-vue

// 2、安装webpack
cnpm install -D webpack webpack-cli

// 3、引入我们需要的第三方依赖包和loader
cnpm install -S vue // 安装vue
cnpm install -D vue-loader vue-template-compiler // vue-loader是必须的，vue-template-compiler是vue-loader必须的依赖
cnpm install -D @babel/core @babel/preset-env @babel/plugin-transform-runtime babel-loader // 安装babel，将es6 -> es5
cnpm install -D css-loader style-loader sass-loader node-sass
cnpm install -D file-loader url-loader // 图片等资源加载器
```

## 配置
***
安装好需要的模块后，我们就需要在webpack.config.js中把这些模块按照一定的方式配置好，然后才能正常的启动项目。

```js
const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    mode: 'development',
    entry: './src/main.js',
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'js/[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            }, {
                test: /\.less$/,
                use:['vue-style-loader','css-loader','less-loader']
            }, {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        'less': ['vue-style-loader', 'css-loader', 'less-loader']
                    }
                }
            }
        ],
        plugins: [
            new VueLoaderPlugin()
        ]
    }
}
```

## 目录结构
***
```js
|   App.vue
|   index.js
|   main.js
|
+---assets
|       logo.jpg
|
+---style
        main.css
```

App.vue
```html
<template>
    <div id="app">
        <img :src="require('@/assets/logo.jpg')" />
        <span>{{ msg }}</span>
        <p class="test">test</p>
    </div>
<template>
<script scoped>
    export default {
        name: 'App',
        data() {
            return {
                msg: 'test',
            }
        },
        created(){},
        mounted(){},
        components:{}
    }
</script>
<style scoped lang="less">
    #app {
        img { width: 100px; height: 100px; }
        .test {
            color: red
        }
    }
</style>
```

main.js
```js
import Vue from 'vue';
import './style/main.css';
import App from './App.vue';

new Vue({
    el: '#App',
    template: '<App/>',
    components: { App }
})
```

我们基本完成了vue开发环境的构建，下面将继续深化这个脚手架工具；让这个脚手架支持更多的特性。

1、首先我们需要修改我们的npm script里面的命令行配置我们的开发环境，还有线上环境，我们通过`cross-env`传递全局变量`NODE_ENV`，然后在配置文件中接收。如下所示:
```js
"dev": "cross-env NODE_ENV=development npx webpack-dev-server --open --hot --hide-modules",
"build": "cross-env NODE_ENV=production npx webpack --progress --hide-modules",
"build-dev": "npx webpack --progress --config webpack.config.js --hide-modules"
```

2、接着，我们就需要在`webpack.config.js`配置文件中接收下这个NODE_ENV.
```js
const Mode = process.env.NODE_ENV ? process.env.NODE_ENV : 'development';
```

3、安装需要的插件
```js
cnpm install webpack-dev-server -D // 启动服务热更新
cnpm install html-webpack-plugin -D // 生成index.html文件
cnpm install mini-css-extract-plugin -D // 剥离css文件及其公共文件
cnpm install optimize-css-assets-webpack-plugin -D // 压缩css文件
cnpm install clean-webpack-plugin -D // 清理dist目录
```

4、接下来我们要在webpack.config.js中引入这些插件
```js
const htmlWebpackPlugin = require('html-webpack-plugin');
const miniCssExtractPlugin = require('mini-css-extract-plugin');
const optimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
```

5、启动服务
```js
devServer: {
    contentBase: path.resolve(__dirname, 'dist'),
    port: 3002,
    open: false,
    hot: true
},
```

6、配置生产环境和线上环境，分别Loader加载
```js
rules: [
    {
        test: /\.js$/,
        loader: 'vue-loader',
        exclude: /node-modules/
    },
    {
        test: /\.css$/.
        use: [Mode == 'development' ? 'style-loader' : miniCssExtractPlugin.loader, 'css-loader', 'less-loader']
    },
    {
        test: /\.vue$/
        loader: 'vue-loader',
        options: {
            loaders: {
                'css': '',
                'less': [Mode == 'development' ? 'vue-style-loader' : miniCssExtractPlugin.loader, 'css-loader', 'less-loader']
            }
        }
    }
]
```

7、加载插件内容
```js
plugins: [
    new webpack.DefinePlugin({
        'process.env': {
            NODE_ENV: '"development"'
        }
    }),
    new VueLoaderPlugin(),
    new htmlWebpackPlugin({
        hash: true,
        filename: 'index.html',
        title: 'webpack-vue',
        template: './index.html'
    }),
    new webpack.HotModuleReplacementPlugin() // 热模块替换 HMR
]
```

8、配置生产环境
```js
if(process.env.NODE_ENV === 'production') {
    module.exports.mode = 'production';
    module.exports.devtool = '#source-map';
    module.exports.output.publicPath = '/';
    module.exports.optimization = {
        minimizer: [new OptimizeCssAssetsPlugin({})],
        splitChunks: {
            cacheGroups: {
                vendor: {
                    name: 'vendor',
                    test: /\.(css|js)$/,
                    chunks: 'all',
                    enforce: true,
                }
            }
        }
    };
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new miniCssExtractPlugin({
            filename: 'css/[name].css',
            chunkFilename: 'css/[name].chunk.css',
        }),
        new CleanWebpackPlugin()
    ])
}
```

9、接下来我们就可以执行npm run build打包我们的项目了。