# 使用Socket.io建立Webocket应用

## WebSocket的优势
1、性能高。

根据测试环境数据的不同，大约比普通ajax请求高2-10倍。HTTP是文本协议，数据量比较大。
而WebSocket是基于二进制的协议，在建立连接时用的虽然是文本数据，但之后传输的都是二进制数据，因此性能比ajax请求高。

2、双向通道
如果是普通ajax请求，需要实时获取数据，只能用计时器定时发送请求，这样会浪费服务器资源和流量。
而通过WebSocket，服务器可以主动向前端发送信息。

3、安全性高
由于WebSocket出现较晚，相比HTTP协议，在安全性上考虑的更加充分。

## Socket.io
Socket.io是在使用WebSocket时的一个常用库，他会自动判断在支持WebSocket的浏览器中使用WebSocket,在其他浏览器中，会使用如flash等方式完成通信。
1、操作简单
2、兼容低端浏览器，如IE6
3、自动进行数据解析
4、自动重连 如果出现连接断开的情况，WebSocket会进行自动重连

## 使用Socket.io建立WebSocket应用

`服务端代码`
```js
const http = require('http');
const io = require('socket.io');

// 建立HTTP服务器
const server = http.createServer((req, res) => {

})

server.listen(8080);
// 建立WebSocket，让socket.io监听HTTP服务器，一旦发现是WebSocket请求，则会自动进行处理。
const ws = io.listen(server);
// 建立连接完成后，触发connection事件
// 该事件会返回一个socket对象(https://socket.io/docs/server-api/#Socket),可以利用socket对象进行发送、接收数据操作。
ws.on('connection', (socket) => {
	// 根据事件名，向客户端发送数据，数据量不限
	socket.emit('msg', '服务端向客户端发送数据第一条', '服务端向客户端发送数据第二条');
	// 根据事件名接收客户端返回的数据
	socket.on('msg', (...msgs) => {
		console.log(msgs);
	})
	//使用定时器向客户端发送数据
	setInterval(() => {
		socket.emit('timer', new Date().getTime())
	}, 500);
})
```

`客户端示例代码/lessions19/index.html`
```js
<html>
<head></head>
<body>
# 引用Socket.io的客户端js文件，由于Socket.io已经在服务端监听了HTTP服务器的请求，一旦收到对该文件的请求，则会自动返回该文件，不需要开发人员配置
# 该文件在服务器的位置为/node_modules/socket.io/node_modules/socket.io-client/dist/socket.io.js
<script>
	const socket = io.connect('ws://localhost:8080');
	socket.emit('msg', '客户端向服务端发送数据第一条', '客户端向服务端发送数据第二条')
	socket.on('msg', (...msgs) => {
		console.log(msgs);
	})
	socket.on('timer', (time) => {
		console.log(time);
	})
</script>
</body>
</html>
```
