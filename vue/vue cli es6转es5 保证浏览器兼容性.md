# vue cli es6转es5 保证浏览器兼容性
***

最近开发了一个项目，开发过程中，由于需要使用async await，于是发现，只有少数浏览器支持，极大多数浏览器是不支持的，在网上找了各种解决方案，基本都是失败，最后总结了两个方案后，尝试成功。

## IE报vuex requires a promise polyfill in this browser问题的解决
第一步: 安装babel-polyfill。babel-polyfill可以模拟es6使用的环境，可以使用es6的所有新方法。
`npm install babel-polyfill -S`

第二步: 在webpack中使用
在webpack.config.js中，使用

```js
module.exports = {
    entry: {
        app: ['babel-polyfill', './src/main.js']
    }
}
```

替换

```js
module.exports = {
    entry: {
        app: './src/main.js'
    }
}
```