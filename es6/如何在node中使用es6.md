# 如何在node中使用es6
***

Node本身已经支持部分es6语法，但是`import`,`export`，以及`async`和`await`(Node8已经支持)等一些语法，我们还无法使用。为了能使用这些特性，我们就需要使用babel把ES6转换成es5语法。

## 安装babel

```js
npm install babel-cli -g
```

## 基础知识
babel的配置文件时.babelrc

```js
{
    "presets": []
}
```

新建一个demo文件夹，文件夹下新建1.js

```js
const arr = [1, 2, 3];
arr.map(item => item + 1);
```

同时新建上文的.babelrc配置文件。
终端运行

```js
babel 1.js -o dist.js
```

可以看见在文件夹下多了一个dist.js，这就是babel转码后的文件，但是,dist.js里是没有任何变化的，因为我们在配置文件里没有声明转码规则，所以babel无法转码。

## 安装转码插件

```js
npm install babel-preset-es2015 babel-preset-stage-0 -D
```

修改配置文件:

```js
{
    "presets": [
        "es2015",
        "stage-0"
    ]
}
```

`es2015`可以转码es2015的语法规则，`stage-0`可以转码es7语法(比如async, await),再次运行终端。
`babel 1.js -o dist.js`

可以看见，箭头函数被转码了。

如果要把1.js和util.js都转码，我们可以把整个文件夹转码。

```js
babel demo -d dist
```
新生成的dist文件夹下，就有转码后的文件，可以看见，转码后，仍然使用的是module.exports 的CMD模块加载。

上面的转码有个缺陷，就是babel会默认把所有的代码都转为es5，这意味着，即使node支持let关键字，转码后也会被转为var。我们可以使用`babel-preset-env`这个插件，他会自动检测当前node版本，只转码node不支持的语法，非常方便。

```js
npm install babel-preset-env -D
```

.babelrc文件

```js
{
    "presets": [
        "env", {
            "target": {
                "node": "current"
            }
        }
    ]
}
```

编译出来后可以看到class和const并没有被转码，因为当前node版本支持该语法，在实际项目中使用es6语法，Koa2需要Node v7.6.0以上的版本来支持async语法，同时，我们也想在Koa2中使用import模块化写法。

```js
npm install babel-register -D
npm install koa -S
```

如果通过`node app`直接启动，肯定报错。我们需要一个入口文件，来转码。
index.js

```js
require('babel-register');
require('./app.js');
node index
```

此时访问`http://localhost:3000`即可看见页面了。
babel-register是实施转码的，所以实际发布时，应该先把整个app文件夹转码.

```js
babel app -d dist
```

这次，只要启动dist下的app.js即可.