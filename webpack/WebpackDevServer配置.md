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

### devServer.compress(boolean类型)
***
对所有请求启用gzip压缩。

```js
compress: true
```

### devServer.contentBase(boolean string array类型)
***
设置server对外服务的内容来源，只有在提供静态文件访问的情况下才需要使用该配置。
devServer.publicPath会被用来设置提供bundles文件的位置，而且会优先考虑该配置的路径。
默认情况下会使用当前运行命令的文件夹作为内容源，可以使用如下配置对此进行更改。

```js
contentBase: path.join(__dirname, 'public')
```
建议使用绝对路径，不要使用相对路径。

禁止使用contentBase可以做如下设置。
```js
contentBase: false
```

### devServer.filename(String)
***
该配置可以配置成lazy mode来减少编译，lazy mode模式下默认会在每次请求时，进行一次编译。使用filename，可以设置当请求某个指定的文件时，才进行编译。如果output.filename被设置为bundle.js并且filename如下使用，则仅仅会在请求bundle.js时，进行编译。

```js
lazy: true,
filename: 'bundle.js'
```

如果是设置了filename而不设置lazy mode，则不会有任何效果。

## devServer.headers(Object)
***
向所有的请求添加headers:
```js
headers: {
    "X-Custom-Foo": "bar"
}
```

## devServer.historyApiFallback(Boolean Object)
***
当使用html5 history api,将会在响应404时返回index.html。想要开启该功能进行如下设置。

```js
historyApiFallback: true
```

通过传递一个Object来对该功能做更多的定制。

```js
historyApiFallback: {
    rewrites: [
        { from: /^\/$/, to: '/views/landing.html' },
        { from: /^\/subpage/, to: '/views/subpage.html' },
        { from: /./, to: '/views/404.html' }
    ]
}
```

当在路径中使用.符号，需要使用disableDotRule配置。

```js
historyApiFallback: {
    disableDotRule: true
}
```

## devServer.hot(String 该配置只能用于CLI)
***
指定使用的host。默认情况下是localhost。
如果希望server被外部访问，需要像下面指定。

```js
host: '0.0.0.0'
```

## devServer.hot(Boolean)
***
启用webpack的Hot Module Replacement特性。

```js
hot: true
```

## devServer.hotOnly(Boolean 只适用于CLI)
***
启用Hot Module Replacement，当编译失败时，不刷新页面。

```js
hotOnly: true
```

## devServer.https(Boolean, Object)
***
默认情况下dev-server使用http协议，通过配置可以支持https。
`https:true`
通过该配置，会使用自签名的证书，同样可以自定义签名证书。

```js
https: {
    key: fs.readFileSync('/path/to/server.key'),
    cert: fs.readFileSync('/path/to/server.crt'),
    ca: fs.readFileSync('/path/to/ca.pem')
}
```

该对象的配置项会直接传递给Node.js的HTTPS模块。

## devServer.inline(Boolean 只适用于CLI)
***
切换dev-server的两种模式，默认情况server使用inline mode。
这种情况下, live reload及构建信息的相关代码会被插入到bundle之中。
另一种模式是iframe mode。使用iframe mode会在通知栏下方显示构建信息，切换到iframe mode可使用下方配置。

```js
inline: false
```

`使用Hot Module Replacement时，建议使用inline mode`

## devServer.lazy(Boolean)
***
当启用lazy,dev-webpack仅在其请求时进行编译。
这意味着webpack不会监控文件改变，所以该模式称为lazy mode。
开启lazy mode模式如下:
`lazy: true`

> 当在lazy 模式下，watchOptions将不会被启用
> 如果在CLI下使用，需要确保inline mode被禁用

## devServer.noInfo(Boolean)
***
启用noInfo，类似webpack bundle启动或保存的信息将会被隐藏，Errors和warnings仍然会被显示。
`noInfo: true`

## devServer.overlay(Boolean Object)
***
在浏览器上全屏显示编译的errors或warnings。
默认是关闭的，如果只想显示编译错误，则如下配置: `overlay: true`
如果即想显示errors也想显示warnings，则如下配置。

```json
overlay: {
    warnings: true,
    errors: true
}
```

## devServer.port(Number 只用于CLI)
***
指定服务监听的端口

```js
port: 8080
```

## devServer.proxy(Object)
***
未来保证在同一域名下，请求一些在其他域名下的api接口时会用到该配置。
dev-server使用http-proxy-middleware包。
当服务运行于`localhost:3000`时，可以使用如下配置启用代理。

```js
proxy: {
    '/api': 'http://localhost:3000'
}
```

对`/api/users`的请求会通过代理请求到`http://localhost:3000/api/users`
如果不想将`/api`传递过去，需要重写path:

```js
proxy: {
    '/api': {
        target: 'http://localhost:3000',
        pathRewrite: {'^/api': ''}
    }
}
```

默认情况下如果请求的服务是https的，并且证书是未认证的，则该未认证证书默认是无法使用的。如果想使用该证书，需要如下配置，关闭安全监测。

```js
proxy: {
    '/api': {
        target: 'https://other-server.com',
        secure: false
    }
}
```

有时候，不希望代理所有请求，可以向bypass属性传递一个function来实现该需求。
在function中，可以获取到request, response及proxy options。
该function必须返回false或返回被部署的文件路径，而不是继续去代理请求。

例子，对于浏览器的请求，只希望提供html网页的访问，而对于api请求，则将请求代理到指定服务。

```js
proxy: {
    '/api': {
        target: 'http://localhost:3000',
        bypass: function(req, res, proxyOptions) {
            if(req.headers.accept.indexOf('html') !== -1) {
                console.log('skip proxy for browser request');
                return '/index.html'
            }
        }
    }
}
```

## devServer.public(String CLI only)
***
当使用inline mode并代理到dev-server，内链的客户端代码不知道该访问哪个域名。他将会基于window.location来连接服务器。但是如果这样做有问题。则需要使用public设置。
例子: dev-server被代理到nginx中配置的myapp.test

```js
public: 'myapp.test:80'
```

## devServer.publicPath(Strign)
***
打包文件将被部署到该配置对应的path。
假设server运行在`http://localhost:8080`而`output.filename`设置位于`bundle.js`。默认情况下`publicPath`为`/`，所以最终生成的bundle文件可以通过如下路径访问。`http://localhost:8080/bundle.js`。
publicPath更改为一个文件夹

```js
publicPath: '/assets/'
```

最终生成文件的访问路径为`http://localhost:8080/assets/bundle.js`。

`publicPath前后的值，必须带斜杠`

也可以使用完整的url进行制定，如果使用HMR则必须使用该种方法。

```js
publicPath: 'http://localhost:8080/assets/'
```

最终生成的文件仍然通过`http://localhost:8080/assets/bundle.js`进行访问。

`建议将devServer.publicPath同output.publicPath配置成相同值`

## devServer.quiet(Boolean)
***
当启用该配置，除了初始化信息会被写到console中，其他任何信息都不会被写进去。
errors和warnings也不会被写到console中。

```js
quiet: true
```

## devServer.setup(Function)
***
通过该function可以访问Express app对象，添加自定义的middleware.
举例，为某个路径添加自定义处理。

```js
setup(app){
    app.get('/some/path', function(req, res) {
        res.json({custom: 'response'})
    })
}
```

## devServer.staticOptions
***
能够对contentBase配置部署的静态文件进行高级配置。

```js
staticOptions: {
    redirect: false
}
```
`注意:该配置仅当contentBase配置为string时起作用`

## devServer.stats(String, Object)
***
略

## devServer.watchContentBase(Boolean)
***
设置server监控通过devServer.contentBase设置的文件
在文件改变时会进行页面刷新，默认情况下该配置是禁止的。

```js
watchContentBase: true
```

## devServer.watchOptions(Object)
***
对文件更改的监控配置。
webpack基于文件系统来获取文件的改变，在某些场景下，是不起作用的。
比如:当使用NFS或Vagrant，针对这种情况使用polling进行监控。

```js
watchOptions: {
    poll: true
}
```

如果该操作对于文件系统来说消耗较大，可以设置在一定的时间间隔内触发一次。