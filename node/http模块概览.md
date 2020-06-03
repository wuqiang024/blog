# http模块概览
在nodejs中http可以说是最核心的模块，同时也是比较复杂的模块。

## 一个简单的例子
在想下面例子中，我们创建了一个服务端，一个http客户端。

* 服务器server: 用来接收客户端的请求，并将客户端请求的地址返回给客户端
* 客户端client: 向服务端发起请求，并将服务端返回的内容打印到控制台

```js
var http = require('http');

var server = http.createServer(function(serverReq, serverRes) {
	var url = serverReq.url;
	serverRes.end('您访问的地址是:' + url);
});

server.listen(3000);

var client = http.get('http://127.0.0.1:3000', function(clientRes) {
	clientRes.pipe(process.stdout);
})
```

## 例子解释
在上面这个简单的例子里，涉及了4个实例，大部分时候，req, res才是主角。

* server: http.Server实例，用来提供服务，处理客户端的请求。
* client: http.clientRequest实例，用来向服务端发起请求
* serverReq/clientRes: 其实都是http.ImcomingMessage实例。serverReq用来获取客户端请求的相关信息，而clientRes用来获取服务端返回的相关信息。
* ServerRes: http.ServerResponse实例

## 关于http.IncomingMessage、http.ServerResponse
先讲一下http.ServerResponse实例，作用很明确，服务端通过http.ServerResponse实例，来给请求端发送数据，包括发送响应头，发送响应主体等。

接下来是http.IncomingMessage实例。
在server端: 获取请求发送方的信息，比如请求方法，路径，传递的数据等。在client端: 获取server端发送过来的信息，比如请求方法，路径，传递的数据等。

http.IncomingMessage实例有三个属性: method, statusCode, statusMessage。

* method: 只在server端的实例有(serverReq.method)
* statusCode/statusMessage: 只在client端的实例有(clientRes.method)

## 关于继承与扩展
### http.Server

* http.Server继承了net.Server
* net.createServer(fn),回调中的socket是个双工的stream接口，也就是说，读取发送方信息，向发送方发送信息都靠他。

备注: socket的客户端、服务端是个相对的概念，所以其实net.Server内部也是用了net.Socket。

```js
var net = require('net');
var HOST = '127.0.0.1', PORT = 8989;

var server = net.createServer(function(socket) {
	console.log(socket.remoteAddress + socket.remotePort);
	socket.on('data', function(data) {
		console.log(data);
		socket.write(data);
	})

	socket.on('close', function() {
		console.log('closed');
	})
});

server.listen(PORT, HOST);
```

## http.ClientRequest
http.ClientRequest内部创建了一个socket来发起请求。
当你调用http.request(options)时，内部是这样的

```js
self.onSocket(net.createConnection(options));
```

## http.ServerResponse
实现了Writable Stream interface，内部也是通过socket来发送信息。

## http.IncomingMessage
实现了Readable Stream interface.
req.socket -> 获得跟这次链接相关的socket 