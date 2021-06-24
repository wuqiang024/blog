# 用ES6编写Webpack的配置文件
***
## 概述
***
目前想在webpack.config.js中使用es6的模块语法，有三种方法可以做到。

## 方法1: 升级到Node.js4
***
Node.js4合并了io.js，所以自然带有所有io.js的特性，其中就包括部分ES6特性的支持。不过目前的版本(4.2.1)只支持部分特性。尤其是以下几个很常用的都不支持:
* 函数默认值
* 解构和其相关的所有功能
* ES6模块

## 方法2: webpack.config.babel.js
***
这个最简单，把webpack.config.js改名为webpack.config.babel.js就行，一切命令照旧。
webpack在执行时会用babel把配置文件转成es6代码再继续处理。一切babel支持的语言特性都可以使用。
这是一个webpack支持，但是文档里没有提到的特性，只要你把配置文件命名为webpack.config.[loader].js，webpack就会用相应的loader去转换一遍配置文件。所以要使用这个方法，你需要安装babel-loader和babel-core两个包。记住你不需要完整的babel包。

理论上这种方法支持任何loader，所以你也可以用coffescript或其他语言去写，只要有相应的loader就行。

这个方法有个好处，如果你在webpack.config.babel.js里import了其他文件，那个文件也会被babel编译。比如:

```js
import config from './some-config'

export default {}
```

不过，如果你打算自己写脚本去加载webpack的配置，这个方法就不管用了。

总结：这个方法适合那些不在乎Node.js版本，只使用webpack和webpack-dev-server命令，不打算自己写脚本或过多折腾，但想使用完整但es6特性但人。

## 方法3: 用babel-node
***
不改名，但是配置文件和各种脚本都是完全的es6语法，这是怎么做到的呢？
关键就在于babel-node。这是babel提供的一个命令后工具，你可以用它代替node去执行。文件会被Babel编译后再交给node命令执行。

首先用`package.json`里定义的`scripts`来代替`webpack`命令。

```json
{
  "scripts": {
    "bundle": "babel-node tools/run bundle"
  }
}
```

这样就可以用`npm run bundle`来执行相应的任务来。这个任务会先调用`tools/run.js`,然后调用`tools/bundle.js`，然后加载`tools/webpack.config.js`。整个流程中的所有文件都是用es6和es7语法写的，非常整洁漂亮。

总结：这个方法适合需要自己写脚本并且想完整使用es6语法的人，不过`babel-node`因为要编译，而且换成结果会存在内存中，所以执行时间会比单纯使用`node`更长（主要是启动时间）。记住不要在生产环境下使用`babel-node`