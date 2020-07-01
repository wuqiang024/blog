# Webpack DevServer配置
***
## DevServer
***
该文档主要描述关于devserver的相关配置。(配置同webpack-dev-middleware兼容)

## devServer(Object类型)
***
该配置会被`webpack-dev-server`使用，并从不同方面做定制。
下面是一个例子，使用gzip提供对dist/文件夹下内容的访问。

```js
devServer: {
    contentBase: path.join(__dirname, 'dist'), // 对外提供的访问内容的路径
    compress: true,  // 启用gzip压缩
    port: 9000, // 提供访问的接口
}
```