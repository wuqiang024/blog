# Node.js搭建http服务器
## 创建server.js

```js
const http = require('http');
const qs = require('querystring');
const url = require('url');

http.createServer(function(req, res) {
	console.log('receive request');
	res.writeHead(200, {'Content-Type': 'text/plain'});
	res.end('hellow world');
}).listen(3000);
```

## 执行server.js

```sh
node server.js
```

## 发送GET请求
### 发送get请求通过聚合服务器获取微信新闻数据

```js
const http = request('http');
const qs =o require('querystring');

http.get('http://v.juhe.cn/weixin/query?key=f16af393a63364b729fd81ed9fdd4b7d&pno=1&ps=10', function(res) {
	var body = [];
	console.log(res.statusCode);
	console.log(res.headers);
	console.log(res);
	res.on('data', function(chunk) {
		body.push(chunk);
	});

	res.on('end', function() {
		body = Buffer.concat(body);
		console.log(body.toString());
	})
})
```

### 发送post请求通过聚合服务器获取微新闻数据

```js
const http = require('http');
const qs = require('querystring');

var postData = qs.stringify({
	'key': 'f16af393a63364b729fd81ed9fdd4b7d',
	'pno': 1,
	'ps': 10
});

var options = {
	hostname: 'v.juhe.cn',
	path: '/weixin/query',
	method: 'POST',
	header: {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': Buffer.byteLength(postData)
	}
};

var req = http.request(options, (res) => {
	console.log(res.statusCode);
	console.log(JSON.stringify(res.headers));
	res.setEncoding('utf8');
	res.on('data', function(chunck) {
		console.log(chunk);
	});
	res.on('end', () => {
		console.log('end')
	})
})

