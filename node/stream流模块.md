## Stream介绍
***
Stream是一个抽象接口，Node中国有很多对象实现了这个接口。例如，对Http服务器发起请求的request对象就是一个Stream，还有stdout(标准输出)。往往用于打开大型的文本文件，创建一个读取操作的数据流。所谓大型的文本文件，指的是文本文件的体积很大，读取操作的缓存装不下，只能分成几次发送，每次发送会触发一个data事件，发送结束会触发end事件。

## 读取流
***
```javascript
var fs = require('fs');
var data = '';

var readerStream = fs.createReadStream('input.txt');
readerStream.setEncoding('utf8');
readerStream.on('data', function(chunk) {
	data += chunk;
});
readerStream.on('end', function() {
	console.log(data);
});
readerStream.on('error', function(err) {
	console.log(err.stack);
})
console.log('程序执行完毕');
```

## 写入流
***
```
var fs = require('fs');
var data = '中国';

var writeStream = fs.createWriteStream('output.txt', {'flag':'a'}); // 追加文本
或
var writeStream = fs.createWriteStream('output.txt');
writeStream.write(data, 'utf8');
writeStream.end()

writeStream.on('finish', function() {
	console.log('写入完成');
})

writeStream.on('error', function(err) {
	console.log(err.stack);
})

console.log('写入流完毕');
```

## 管道流
***
管道提供了一个输出流到输入流的机制。通常我们用于从一个流中获取数据并将数据传递到另一个流中，我们把文件比作装水的桶，而水就是里面的内容。我们用一根管子(pipe)链接两个桶，使得水从其中一个桶流入另一个桶，这样就慢慢的实现了大文件的复制过程。
```javascript
var fs = require('fs');
var readerStream = fs.createReadStream('input.txt');
var writeStream = fs.createWriteStream('out.txt');
readerStream.pipe(writeStream);
console.log('程序执行完毕');
```

## 链式流
***
链式是通过连接输出流到另外一个流并创建多个对流操作链的机制。链式流一般用于管道操作。接下来我们就用管道和链式来压缩和解压文件。

### 压缩
```javascript
var fs = require('fs');
var zlib = require('zlib');

fs.createReadStream('input.txt')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('input.zip'));
```

### 解压
```javascript
var fs = require('fs');
var gzip = require('gzip');

fs.createReadStream('input.zip')
  .pipe(zlib.createGunzip())
  .pipe(fs.createWriteStream('out.txt'));
```

## 服务器gzip压缩
代码超级简单。首先判断是否包含accept-encoding首部，并且值为gzip。
* 否: 返回未压缩的文件
* 是: 返回压缩的文件

```js
var http = require('http');
var zlib = require('zlib');
var fs = require('fs');
var filepath = './extra/fileForGzip.html';

var server = http.createServer(function(req, res) {
	var acceptEncoding = req.headers['accept-encoding'];
	var gzip;

	if(acceptEncoding.indexOf('gzip') != -1) {
		gzip = zlib.createGzip();
		res.writeHead(200, {'Content-Encoding':'gzip'});
		fs.createReadStream(filepath).pipe(gzip).pipe(res);
	} else {
		fs.createReadStream(filepath).pipe(res);
	}
});
server.listen(3000);
```

## 服务端字符串gzip压缩
代码跟前面例子大同小异。这里采用了zlib.gzipSync(str)对字符串进行gzip压缩。
```js
const http = require('http');
const fs = require('fs');
const zlib = require('zlib');
const filepath = './extra/fileForGzip.html';
const responseText = 'hello world';

const server = http.createServer(function(req, res) {
	var acceptEncoding = req.headers['accept-encoding'];
	res.writeHead(200, {'content-encoding':'gzip'});
	res.end(zlib.gzipSync(fs.createReadStream(responseText)))
})
```