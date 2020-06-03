关于Socket hang up 最早是在一次服务器压测中出现的，后来得到了解决，近期在Node.js服务迁移K8S容器中时又报出了此问题。核查之后发现是对容器的CPU,内存大小做了限制引起的，这里总结下什么是Socket hang up以及在什么情况下发生，该如何解决。

# 什么是Socket hang up
hang up翻译为英文也有挂断的意思，socket hang up也可以理解为socket(链接)被挂断。无论使用哪种语言，也许多多少少应该会遇见过，只是不知道你有没有去思考这是为什么? 例如在nodejs系统中提供的http server默认超时为2分钟(server.timeout)可以查看，如果一个请求超过这个时间，http server会关闭这个请求连接，当客户端想要返回一个请求的时候发现这个socket已经被挂断，就会报hang up错误。

# 复现 Socket hang up
服务端
开启一个http服务，定义/timeout 接口设置3分钟后延迟响应

```js
const http = require('http');
const port = 3000;
const server = http.createServer((req, res) => {
	console.log('request url:' + req.url);
	if(request.url === '/timeout') {
		setTimeout(function() {
			res.end('ok')
		}, 1000 * 60 * 3)
	}
}).listen(port);
console.log('server listening on port:' + port);
```

客户端

```js
const http = require('http');
const opts = {
	hostname: '127.0.0.1',
	port: 3000,
	path: '/timeout',
	method: 'GET'
};

http.get(opts, (res) => {
	let rawData = '';
	res.on('data', function(chunk) {
		rawData += chunk;
	})

	res.on('end', ()=> {
		try {
			console.log(rawData);
		} catch (e) {
			 console.error(e)
		}
	}).on('error', err => {
		console.error(err);
	})
})
```

启动服务端后再启动客户端大约2分钟后或者直接kill掉服务端，会报如下错误，可以看到相应的错误堆栈。

```js
Error: socket hang up
    at connResetException (internal/errors.js:570:14)
    at Socket.socketOnEnd (_http_client.js:440:23)
    at Socket.emit (events.js:215:7)
    at endReadableNT (_stream_readable.js:1183:12)
    at processTicksAndRejections (internal/process/task_queues.js:80:21) {
  code: 'ECONNRESET'
}
```

为什么在http client这一端会报socket hang up这个错误，看下Node.js http client端源代码会发现由于没有得到响应，那么就认为这个socket已经结束，因此会在L440处触发一个connResetException('socket hang up')错误。

# socket hang up以及在什么情况下发生，该如何解决。
1、设置http server socket超时时间
看下http server源代码，默认情况下服务器的超时时间为2分钟，如果超时，socket会自动销毁，可以通过调用server.setTimeout(msecs)方法将超时时间调节的大一点，如果传入0则关闭超时机制。

```js
const server = http.createServer((req, res) => {
	console.log(req.url);
	setTimeout(function() {
		res.end('ok');
	}, 1000 * 60 * 3)
})

# ECONNRESET VS ETIMEDOUT
ECONNRESET为读取超时，当服务器太慢无法响应时就会发生{ "code": "ECONNRESET" }错误，例如上面介绍的socket hang up例子。
ETIMEDOUT为链接超时，是指的在客户端与远程服务器建立链接时发生的超时，下面给一个request模块的例子。

```js
const request = require('request');
request({
	url: 'http://127.0.0.1/timeout',
	timeout: 5000,
}, (err, response, body) => {
	console.log(err, body);
})
```

以上示例，大约持续5秒后会报{ "code": "ETIMEDOUT" }错误，堆栈如下。

略...