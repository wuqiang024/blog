# 原生node的header
首先引入http模块

获取http.ServerResponse对象的方式。

1、http.createServer(function(req, res) {})，其中res是http.ServerResponse对象
2、var server = http.createServer().listen(3000, 'localhost');
server.on('request', function(req, res) {}); server的request对象的request事件中，res为http.ServerResponse对象

http.ServerResponse对象的方法。

## 报头
writeHead()
setHeader()
getHeader(类型参数)
removeHeader()
addTrailers() 追加头信息

## 报文
write() 报文内容，返回值是true/false
end() 结束响应，必须调用end()方法，否则时超时，没有响应
setTimeout() 服务器没有响应时，触发这个事件

## http.ServerResposne对象的属性
headerSent  当头部已经有响应后，res.headerSent为true，否则为false。可以通过这个属性来判断是否已经响应。
statusCode  状态码
sendDate  true/false，当为false时，将删除头部时间。

## http.ServerResponse监听的事件
1、timeout事件
2、close事件
3、request事件
4、checkContinue事件
5、connect事件
6、clientError事件

## 设置头部信息，有两个方法
1、setHeader(name, value)方法可以调用多次，但真正写入到头部的必须调用一次writeHead()
2、http.ServerResponse.writeHead(statusCode, {name: value})
3、设置的头部信息的内容
Content-Type: 内容类型
Location: 将客户端的请求重定向
Content-Disposition: 指定一个被下载的文件名
Content-Length: 服务器响应的字节数
Set-Cookie: 设置cookie
Cache-Control: 开启缓存
Expires: 缓存失效时间
Etag: 当服务器没什么变化时，不重新下载文件。

```js
res.writeHead(200, [
    ['Set-Cookie', 'mycookie1=value1'],
    ['Set-Cookie', 'mycookie2=value2']
]);
```

```js
res.setHeader('Set-Cookie', [ 'mycookie1=value1',  'mycookie2=value2']);
```

## Content-Type的类型，这是几个大类，然后还有具体的小类
Text: 用于标准化地表的文本信息，文本信息可以是多种字符集或多种格式的
Multipart: 用于连接消息体的多个部分构成一个消息，这些部分可以是不同类型的数据
Application: 用于传输应用程序数据或二进制数据
Message: 用于包装一个E-mail消息
Image: 用于传输静态图片数据
Audio: 用于传输音频或声音数据
Video: 用于传输动态影像数据，可以是与音频编辑在一起的视频数据格式

## 通常还可以设置一些跨域的内容
res.setHeader('Access-Control-Allow-Origin');
res.setHeader('Access-Control-Allow-Headers', 'X-Request-With');
res.setHeader('Access-Control-Allow-Methods', 'POST,GET,DELETE,PUT,OPTIONS');

## 报文信息
在调用res.end()之前可以多次调用res.write()方法，res.write()方法返回一个true/false
当没有响应或者超时时(这种情况遇到多次，进程没有挂掉，一直处于无响应，但是客户端一直可以请求),res.setTimeout(毫秒数，callback)，当超时时，会触发res.on(timeout, function() {}),如果没有回调函数，则自动调用end()结束请求。
当网络较好，数据量较少时，将数据直接发送到操作系统的内核缓存区，然后从内核缓存区去取出数据发送给对付，返回值是true.
当数据量较大，网速较慢时，先将数据缓存在内存中，如果客户端可以接收数据了，再将数据发送到内核缓存区，最后发送给对方。返回值是false。
因此在大量数据的时候，会有内存爆满。
这是在并发情况下的用async做的控制

## 获取req的报文信息
通过req.来获取
1、req.method 客户端请求的方法
2、req.url 客户端请求的url
3、req.headers 客户端请求头对象

## 获取部分内容
在头部中设置:

1.Range: bytes=5001-10000   //5001-10000字节

2.Range: bytes=5001-           //5001字节以后的

3.Range: bytes=-3000,5000-7000 //从一开始到3000字节和5000-7000字节