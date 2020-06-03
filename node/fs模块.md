## 文件模块fs
***
出于安全考虑，javascript不能操作本地文件，所以文件的处理都会放到服务端去处理。Node.js作为一门后端动态语言，同样具备了操作文件的功能，这需要用到node.js的原生模块fs。

## 读取文件--异步读取
***
```javascript
var fs = require('fs');
fs.readFile('demoFile.txt', 'utf8' function(error, data) {
	if(error) {
		return console.error(error);
	}
	console.log(data.toString());
})
```

## 读取文本--同步读取
```javascript
var fs = require('fs');
var data = fs.readFileSync('demoFile.txt');
console.log(data.toString());
```

## 写入文本--覆盖写入
***
```javascript
var fs = require('fs');
fs.writeFile('input.txt', '内容', function(err) {
	if(err) {
		return console.error(err);
	}
})
```

## 通过文件流读取
```js
const fs = require('fs');
const readStream = fs.createReadStream(path, 'utf8');
readStream.on('data', function(chunk) {
	console.log(chunk);
}).on('error', function(err) {
	console.log(err.message);
}).on('end', function() {
	console.log('没有数据了')
}).on('close', function() {
	console.log('已经关闭');
})
```

## 写入文本--追加写入
```js
fs.appendFile('input.txt', '内容', function(err) {
	if(err) {
		return console.error(err);
	}
})
```

## 图片读取
***
图片读取不同于文本，因为文本可以直接用console.log()打印，但是图片需要在浏览器中显示，所以需要先搭建web服务，然后以字节方式读取图片在浏览器中显示。
1、图片读取方式是以字节的方式
2、图片在浏览器的渲染因为没有img标签，所以需要设置响应头为image
```javascript
var http = require('http');
var fs = require('fs');
var content = fs.readFileSync('001.jpg', 'binary');

http.createServer(function(req, res) {
	res.setHeader(200, {'Content-Type', 'image/jpeg'});
	res.write(content, 'binary');
	res.end();
}).listen(8888);
```

## 文件是否存在
fs.exists()已经是deprecated状态，现在可以通过下面代码判断文件是否存在。

```js
const fs = require('fs');
fs.access(filePath, function(err) {
	if(err) throw err;
	console.log('存在')
});
```

fs.access()除了判断文件是否存在(默认模式),还可以用来判断文件的权限。

`备忘: fs.constants.F_OK等常量无法获取(node v6.1, mac 10.11.4下, fs.constants是undefined)`

## 创建目录
异步版本，如果目录存在会报错

```js
var fs = require('fs');
fs.mkdir('./hello', function(err) {
	if(err) throw err;
	console.log('目录创建成功');
})
```

同步版本:

```js
var fs = require('fs');
fs.mkdirSync('./hello');
```

## 删除文件

```js
const fs = require('fs');
fs.unlink('./file.txt', function(err) {
	if(err) throw err;
	console.log('文件删除成功');
});
```

```js
const fs = require('fs');
fs.unlinkSync('./file.txt')
```

## 遍历目录
同步版本，注意: fs.readdirSync()只会读一层，所以需要判断文件类型是否目录，如果是，则进行递归遍历。

```js
const fs = require('fs');
const path = require('path');

const getFilesInfo = function(dir) {
	var results = [path.resolve(dir)];
	var files = fs.readdirSync(dir, 'utf8');
	files.forEach(function(file) {
		file = path.resolve(dir, file);
		var stats = fs.statSync(file);

		if(stats.isFile) {
			results.push(file);
		} else if(stats.isDirectory()) {
			results = results.concat(getFilesInfo(file));
		}
	})
	return results;
}
var files = getFilesInfo('../');
console.log(files);
```

## 文件重命名

```js
const fs = require('fs');

fs.rename('./hello', './world', function(err) {
	if(err) throw err;
	console.log('重命名成功');
})

fs.renameSync(oldPath, newPath)
```

## 监听文件修改

`fs.watch()比fs.watchFile()高效很多`

### fs.watchFile
实现原理: 轮询。每隔一段时间检查文件是否发生变化。所以在不同平台上表现基本是一致的。

```js
const fs = require('fs');
const options = {
	persistent: true, // 默认就是true
	interval: 2000 // 多久检查一次
};
fs.watchFile(filename, options, function(cur, pre) {
	console.log('修改时间为' + cur.mtime);
})
```

## 获取文件状态
区别:
* fs.stat() vs fs.fstat(): 传文件路径与传文件句柄
* fs.stat() vs fs.fstat(): 如果文件是软链接，那么fs.stat()返回目标文件的状态，fs.lstat()返回软链接本身的状态。

* stats.isFile()  -> 是否是文件
* stats.isDirectory() -> 是否是路径
* stats.isSocket() -> 是否是socket文件
* atime: Access Time 访问时间
* mtime: Modified Time 文件内容修改时间
* ctime: 文件状态修改时间，比如修改文件所有者，修改权限，重命名等
* birthtime: Brith Time 创建时间，在某些系统上不靠谱，因为拿不到
* stats.size  大小

## 删除目录
fs.rmdir(path, cb); fs.rmdirSync(path)

```js
const fs = require('fs');
fs.rmdir('./dir', function(err) {
	if(err) throw err;
	console.log('目录删除成功')
})
```