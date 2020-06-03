随着项目越来越多，代码共享必不可少，可以采取的方案是:
1、把公共组件拿出来，开一个新仓库
2、使用webpack进行打包编译，`libraryTarget:'umd'`
3、将打包编译的代码一起提交到仓库
4、使用 `npm install <owner>/<repo> -S`安装依赖，因为仓库均为私有，所以不能发布到NPM
这套方案简单好用，实操效果良好。

## @babel/preset-env
首先，Babel推荐使用`@babel/preset/env`套件来处理转译需求，顾名思义，preset即`预制套件`，包含了各种可能用到的转译工具。之前的以年份为准的preset已经废弃了，现在统一用这个总包。
同时，babel已经放弃开发stage-*包，以后的转译组件都只会放进preset-env包里。

## browserslist
@babel/preset-env支持一些参数，用来处理哪些feature要转译，哪些不用。其中比较重要的是targets，用来指定目标环境。targets使用`browserslist`来筛选浏览器环境，这样我们就不需要指定所有浏览器版本，而可以使用类似`last 2 versions`这样的描述。

如果你想知道自己配置的是否合适，可以在仓库目录下执行npx browserslist`，列出所有目标浏览器。
Babel官方建议我们把targets写到`.browserslistrc`或`package.json`中，这样其他工具也能更轻易的获取到目标浏览器。另外，`npx browserslist`无法从`.babelrc`中读取配置，所以执行的时候看到的会是默认结果。

## useBuiltIns
接下来，我们可以配置useBuiltIns，这个属性决定是否引入polyfill。他有三个可选值，默认是false,即不引入，或者说Babel编译结果不引入，把引入的位置，引入哪些polyfill交给用户处理。因为我们的页面中通常有大量js,在每个文件里分别引入polyfill太浪费资源，所以可以在核心入口js引入一次即可。

但是这样我们必须手动`import '@babel/polyfill'`引入所有polyfill，其实并不理想。因为大多数浏览器不需要这些。
所以推荐使用`useBuiltIns: 'usage'`，即按需引入，虽然文档中标记为experimental，但是用起来没遇到什么问题。如果浏览器不支持所需要的feature，那么就引入polyfill,不然的话就不引入。由于目前打包工具越发智能，随着tree-shaking的完善，这样可以最低限度引入Polyfill。

## core-js
core-js最新版本为3.0.1。core-js2封版于1.5年前，所以里面只有对1.5年前的feature的polyfill，最新1.5年新增的feature都不支持，也就存在因为新功能没有polyfill于是在旧浏览器里失败的风险。
所以我们应当升级到最新版,`npm install core-js@3 -D`，然后修改babel设置。

```js
{
    "presets": [
        [
            "@babel/preset-env",
            {
                "targets": "> 5%",
                "useBuiltIns": "usage",
                "corejs": 3
            }
        ]
    ]
}
```

注意，目前Vue Cli3集成了core-js 2，不支持升级到v3，无法手动升级，需要等待Vue Cli 4。

## @Babel/polyfill
@babel/polyfill是对core-js的封装，引用了core-js的内容和生成器(regenerator-runtime)。v7.4之后，这个仓库就被废弃了，希望用户自己选择使用哪个兼容库。
换言之，以前:
`import "@babel/polyfill";`
现在需要被替换成:
`import "core-js/stable"`;
`import "regenerator-runtime/runtime"`;

不过不建议这样做，对于绝大部分情况，使用
@babel/preset-env + `useBuiltIns: 'usage'`仍然是最好的选择。