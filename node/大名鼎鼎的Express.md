Express是Node.js中一个简单，灵活，强大的Web应用框架。
他提供了一系列强大的特性，可以帮助我们快速创建各种应用，也可以用来编写各种的Web工具。

# 示例
```js
const express = require('express');
const app = express();

const server = app.listen(8000, function() {
	var address = server.address().address;
	var port = server.address().port;
	console.log(address, port);
});

```

# Request对象
request对象表示HTTP请求，包含了请求查询字符串，参数，内容，HTTP头部等属性。常见属性如下:

* req.app: 当callback为外部文件时，用req.app访问express的实例
* req.baseUrl: 获取路由当前安装的URL路径
* req.body/req.cookies: 获取请求主体/cookies
* req.fresh/req.stale: 判断请求是否还新鲜
* req.hostname/req.ip: 获取主机名和IP地址
* req.originalUrl: 获取原始请求URL
* req.params: 获取路由的parameters
* req.path: 获取请求路径
* req.protocol: 获取协议类型
* req.query: 获取URL的查询参数串
* req.route: 获取当前匹配的路由
* req.subdomains: 获取子域名
* req.accepts(): 检查可接受的请求的文档类型
* req.get(): 获取指定的HTTP请求头
* req.is(): 判断请求头Conten

# Response对象
response对象表示HTTP响应，即在收到请求时向客户端发送的HTTP响应数据。常见属性有:
* res.app: 同req.app一样
* res.set()在res.append()后将重置之前设置的头
* res.cookie(name, value): 设置cookie
* res.clearCookie(): 清除cookie
* res.download(): 传送指定路径的文件
* res.get(): 返回指定的HTTP头
* res.json(): 传送json响应
* res.jsonp(): 传送jsonp响应
* res.location(): 只设置响应的Location HTTP头，不设置状态码或close response
* res.redirect(): 设置响应的Location HTTP头，并且设置状态码302
* res.render(view,[locals],callback): 渲染一个view，同时向callback传递渲染后的字符串，如果在渲染过程中有错误发生next(err)将会被自动调用。callback将会被传入一个可能发生的错误以及渲染后的页面，这样就不会自动输出了。
* res.send(): 传送HTTP响应
* res.sendFile(): 传送指定路径的文件，会自动根据文件extension设定Content-Type
* res.set(): 设置HTTP头，传入object可以一次设置多个头。
* res.status(): 设置HTTP状态码
* res.type(): 设置Content-Type的MIME类型。