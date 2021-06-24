## 概览
做过web优化的同学，对性能优化大杀器gzip应该并不陌生。浏览器向服务器发起资源请求，比如下载一个js文件，服务器先对资源进行压缩，
再返回给浏览器，以此节省流量，加快访问速度。
浏览器通过HTTP请求头部里加上Accept-Encoding，告诉服务器，你可以用gzip，或者deflate算法压缩资源。
`Accept-Encoding:gzip, deflate`


## 入门实例：简单的压缩/解压缩
***

### 压缩的例子

```
var fs = require('fs');
var zlib = require('zlib');
var gzip = zlib.createGzip();
var inFile = fs.createReadStream('./extra/fileForCompress.txt');
var out = fs.createWriteStream('./extra/fileForCompress.txt.gz');
inFile.pipe(gzip).pipe(out);
```

### 解压缩的例子

```
var fs = require('fs');
var zlib = require('zlib');
var gzip = zlib.createGunzip();
var inFile = fs.createReadStream('./extra/fileForCompress.txt.gz');
var out = fs.createWriteStream('./extra/fileForCompress.txt');
inFile.pipe(gzip).pipe(out);
```

## 服务端gzip压缩
***
代码很简单，首先判断是否包含accept-encoding收不，并且为gzip。
* 否：返回未压缩的文件。
* 是：返回压缩的文件

```
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
		fs.createReadStream(filepath).pipd(res);
	}
})
```

## 服务器端字符串gzip压缩
***
var http = require('http');
var zlib = require('zlib');

var responseText = 'hello world';

var server = http.createServer(function(req, res){
    var acceptEncoding = req.headers['accept-encoding'];
    if(acceptEncoding.indexOf('gzip')!=-1){
        res.writeHead(200, {
            'content-encoding': 'gzip'
        });
        res.end( zlib.gzipSync(responseText) );
    }else{
        res.end(responseText);
    }

});

server.listen('3000');

```