# Request对象
常见属性有
```js
req.app: // 当callback为外部文件时，用req.app访问express的实例
req.baseUrl: // 获取路由当前安装的URL路径
req.body/req.cookies: // 获取请求主体/Cookies
req.fresh/req.stale: // 判断请求是否还新鲜
req.hostname/req.ip: // 获取主机名和IP地址
req.originUrl: // 获取原始请求URL
req.params: // 获取路由的parameters
req.path: // 获取请求路径
req.protoco: // 获取协议类型
req.query: // 获取URL的查询参数
req.route: // 获取当前匹配的路由
req.subdomains: // 获取子域名
req.accepts(): // 检查请求的Accept头的请求类型
req.acceptsCharsets/req.acceptsEncodings/req.acceptsLnaguages
req.get(): // 获取指定的HTTP头
req.is() // 判断请求头Content-Type的MIME类型
```

# Response对象
常见属性有
```js
res.app: // 同req.app一样
res.append(): // 添加指定HTTP头
res.set(): // 在res.append()之后将重置之前设置的头
res.cookie(name, value): // 设置cookie
res.clearCookie(): // 清除Cookie
res.download(): // 传送指定路径的文件
res.get(): // 返回指定的HTTP头
res.json(): // 传送json响应
res.jsonp(): // 传送jsonp响应
res.location(): // 只设置响应的Location HTTP头，不设置状态码或close response
res.redirect(): // 设置响应的Location HTTP头，并且设置状态码302
res.sendFile(): // 传送指定路径的文件，会自动根据文件extension设定Content-Type
res.set(): // 设置HTTP头，传入object可以一次设置多个头
res.status(): // 设置HTTP状态码
res.type(): // 设置Content-Type的MIME类型
```