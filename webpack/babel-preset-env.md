# babel-preset-env： 一个帮你配置babel的preset
babel-preset-env是一个帮你配置babel的preset，根据配置的目标环境自动采用需要的babel插件。

## 问题
目前，几个presets就能让你确定babel应该支持哪些功能:
`babel-preset-es2015`，`babel-preset-es2016`等: 支持不同版本的es规范。es2015转译了ES6比E5新的特性，es2016转译了ES2016比2015新的特性。
`babel-preset-latest`: 支持现有所有ES版本的新特性，包括处于stage-4里的特性(已经确定的规范，将被添加到下个年度的)。
问题是这些presets有时候做的多余了，举个例子，大部分现代浏览器都已经支持ES6的generator了，但是你如果设置了babel-preset-es2015，generator函数还是会被转译成复杂的es5代码。

## 解决方案
babel-preset-env 功能类似babel-preset-latest，优点是他会根据目标环境选择不支持的新特性来转译。
note: 实验室的属性(babel-preset-latest不支持的)需要手动安装配置相应的plugins或者presets。这样你不再需要es20xx presets了。

## 浏览器
你可以选择指定相应的浏览器配置:
browsers参数在这里查询`https://github.com/ai/browserslist`。举个例子:
支持每个浏览器最近的两个ban'b 和IE大于等于7的版本所需的polyfill和代码转译。

```js
"babel": {
    "presets": [
        "env",
        {
            "targets": {
                "browsers": ["last 2 versions", "ie >= 7"]
            }
        }
    ]
}
```

支持市场份额超过5%的浏览器。
```js
"targets": {
    "browsers": "> 5%"
}
```

指定浏览器版本:
```js
"targets": {
    "chrome": 56
}
```

## Node.js
如果你通过Babel编译你的Nodejs代码，babel-preset-env很有用，设置"targets.node"是"current"，支持的是当前运行版本的node.js:

```js
"babel": {
    "presets": [
        "env",
        {
            "targets": {
                "node": "current"
            }
        }
    ]
}
```
`参看测试Node参数的例子` https://github.com/rauschma/async-iter-demo;

## 其他配置
下面会例举babel-preset-env部分常用配置。所有配置请查看点击https://babeljs.cn/docs/plugins/preset-env/。

### modules(string, 默认值: "commonjs")
将es6模块语法转换成另一种模块类型，可选值:
各种流行的模块化规范: "amd", "commonjs", "systemjs", "umd"
禁止转译: false

### include, exclude(Array of strings, 默认值[])
include: 必须要转译的功能(比如覆盖有故障的本地功能)。跟单独启用相应插件是一样的。
exclude: 禁止转译的功能

## useBuiltIns(boolen, 默认false)
babel为标准库中的新功能提供了polyfill，为内置对象，静态方法，实例方法，生成器函数提供支持。babel-preset-env可以实现基于特定环境引入需要的polyfill。
两种使用方法:

`core-js`,根据需要引入es5,es6+标准方法的实现。
安装polyfill: npm install core-js -S
引入polyfill: import 'core-js'

`babel-polyfill`包含`core-js`和`regenerate-runtime`（提供async语法编译后的运行时环境)。
安装polyfill: npm install babel-polyfill -S
引入polyfill: import 'babel-polyfill';

两种方法最终都会根据环境转译成特定的polyfill。

note:
在整个应用里只能引入一次polyfill，可以在main模块里一次引入。
useBuiltIns会使浏览器下载的代码变少(最终打包的文件大小变小了)。但是不会节约内存，因为polyfill本身只会安装缺少的部分。
更多的Polyfill请参考https://leanpub.com/setting-up-es6/read#ch_babel-helpers-standard-library

## debug(boolean, default: false)
以下内容都会用console.log输出。
* 目标环境
* 启用的transforms
* 启用的plugins
* 启用的polyfills
尝试下面的示例，瞧瞧console输出。

举例:
{
    "presets": [
        "env", {
            "targets": {
                "browsers": "> 5%"
            },
            "modules": false,
            "useBuiltIns": true,
            "debug": true
        }
    ]
}
```
模块不会被转译，可以将import和export交给webpack去处理。
debug输出如下:

```js
Using targets:
{
  "safari": 10
}

Modules transform: false

Using plugins:
  transform-exponentiation-operator {}
  transform-async-to-generator {}

Using polyfills:
  es7.object.values {}
  es7.object.entries {}
  es7.object.get-own-property-descriptors {}
  web.timers {}
  web.immediate {}
  web.dom.iterable {}
  ```

## env是如何基于目标环境去匹配哪些是需要转译的?
根据以下外部数据来确定目标环境支持的情况，可以定期执行build-data.js来生成plugins.json。
* ECMAScript标准兼容列表compat-table。
* plugins包含特性列表plugins-features.js。
* browserslist。

## 下一步还能做什么？
### 有可以访问环境的插件
未来计划让插件拥有检查当前环境具备什么可能性的能力，有两个好处:
1、一些plugins(比如对象扩展运算符)目前通过选项告诉他们是否使用本地功能或Polyfill，如果能知道当前环境，就不需要配置了。
2、基于babel的minifiers可以确定是否可以输出，比如，箭头函数。

## 简化presets
基于ECMAScript版本的presets(es2015等)很多都已经过时了，Babel团队考虑会在未来的版本中移除他们(比如，通过废弃处理)。
基于TC39不同阶段的提案的presets(stage-0等)也是去除的候选，因为在这些stages中的标准是不停的变化的。