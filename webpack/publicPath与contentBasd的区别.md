# webpack配置文件中publicPath和contentBase的区别
***
## publicPath
***
在前端webpack的配置项中publicPath主要出现在两个地方:
* output资源配置输出项中
* devServer静态资源服务配置项中

这两个publicPath有什么区别呢？一句话，output中的publicPath影响资源生成路径，devServer中的publicPath影响资源在本地开发环境中的访问。

在output资源输出配置中通常我们能看到类似下面这样的配置
`config.js`

```js
module.exports = {
    dev: {
        publicPath: '/assets/'
    },
    build: {
        publicPath: 'https://csdn.cdn.cn'
    }
}
```

`webpack.config.js`
```js
module.exports = {
    output: {
        publicPath: process.env.NODE_ENV == 'development' ? config.dev.publicPath : config.build.publicPath
    }
}
```

这样配置好后打包出来的静态资源在html文件中的效果就像这样:
本地开发环境下:
![https://img-blog.csdnimg.cn/20190109184814100.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmc4MzkzMDU5Mzk=,size_16,color_FFFFFF,t_70](https://img-blog.csdnimg.cn/20190109184814100.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmc4MzkzMDU5Mzk=,size_16,color_FFFFFF,t_70)

在生产环境如下:
![https://img-blog.csdnimg.cn/20190109185246370.PNG](https://img-blog.csdnimg.cn/20190109185246370.PNG)

可以看出来publicPath的效果最终体现在静态资源的uri中，在这里区分了运行环境。在本地开发环境用静态资源所在目录相对地址，这里需要注意在publicPath是我们应该写成/publicPath/，不然html页面在访问生成静态资源路径时可能会出现找不到资源的问题。在生产环境时，有时候我们需要将我们的静态资源进行CDN托管。这个时候我们只需将config.build.publicPath换成CDN地址就好了。这样很好的区分开生产环境和本地开发环境静态资源的路径问题。

这样配置好以后，往往伴随而来的是另一个问题，那就是在启动本地服务进行开发调试的时候，会出现静态资源找不到的问题。在解决这个问题之前先来看一下本地服务在webpack中的配置项:

```js
const path = require('path');
module.exports = {
    devServer: {
        port: 8080,
        contentBase: path.join(__dirname, '..', dist),
        publicPath: '',
    }
}
```
如果我们不配置publicPath，我们在启动本地服务后访问http://127.0.0.1:8080/，能访问到我们的默认首页，但是我们打开调试窗口的时候发现静态资源会出现404的问题，但是如果将这里的publicPath配置成output的publicPath，这个时候静态资源就能成功加载了。这是怎么回事呢?

```js
const express = require("express");
const app = express();
const path = require("path");
app.use(express.static('public',path.join(__dirname,'/static')));
app.listen(8080,(err)=>{
   if(err) throw err;
   console.log('server is listening on port 8080')
})
```

这个时候，访问`http://127.0.0.1:8080.public/***.js，能访问到对应static目录下的静态资源。这里使用了一个静态资源中间件static。这句话的作用就是本地服务会拦截所有public开头的uri,然后到static目录下去寻找静态资源，找到就返回。实际上在服务器上是没有public目录的，这里的public可以很好的隐藏我们静态资源在服务器上的实际目录。另一方面，也可以对静态进行分类存放。
devServer中的publicPath其实就是相当于上面express代码中public值的变量。

所以，这两个publicPath基本上是连体兄弟，如果在本地开发环境中配置了output的publicPath,那么在devServer中也要做相应的配置。

## contentBase
***
contentBase代表html页面所在的相对目录，如果我们不配置项，devServer默认html所在的目录就是项目的根目录，这个时候启动服务，访问地址通常会出现下面这样的场面。

![https://img-blog.csdnimg.cn/20190109193049291.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmc4MzkzMDU5Mzk=,size_16,color_FFFFFF,t_70](https://img-blog.csdnimg.cn/20190109193049291.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmc4MzkzMDU5Mzk=,size_16,color_FFFFFF,t_70)

并不会看见html页面，相反展现在我们面前的是项目根目录文件夹，因为我们根目录下根本没有html文件。这个时候html在编译后实际是在dist目录下，所以我们需要这样配置:
```js
devServer: {
    contentBase: 'dist',
}
```

这样我们就能正常访问我们的页面了。

这里需要注意一点，contentBase的路径是相对于webpack.config.js文件所在的目录的，有的时候，我们习惯将webpack配置文件统一放到一个build文件下，这个时候我们在写contentBase路径的时候就需要注意了。

`总结:`
1、output的publicPath是用来给生成的静态资源路径添加前缀的
2、devServer中的publicPath是用来给本地服务拦截publicPath开头的请求的
3、contentBase是用来指定被访问html页面所在目录的
