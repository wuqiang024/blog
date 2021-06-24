图片上传是web开发中常用到的功能，常用的开源组件有multer, formidable等。

## 环境初始化
***
```bash
npm install multer -S
```

## 基础例子：单图上传
app.js

```javascript
var fs = require('fs');
var express = require('express');
var multer = require('multer');
var app = express();
var upload = multer({ dest: 'upload/' });

// 单图上传
app.post('/upload', upload.single('logo'), function(req, res, next) {
	res.send({ret_code: '0'});
})

app.get('/form', function(req, res, next) {
	var form = fs.readFileSync('./form.html', {encoding: 'utf8'});
	res.send(form);
})

app.listen(3000);
```

form.html

```javascript
<form action="/upload" method="post" enctype="multipart/form-data">
	<h2>单图上传</h2>
	<input type="file" name="logo">
	<input type="submit" value="提交">
</form>
```

## 基础例子：多图上传
将前面的upload.single('logo') 改成upload.array('logo',2)就行，表示同时支持两张图片上传，并且name属性为logo。
app.js

```javascript
var fs = require('fs');
var express = require('express');
var multer = require('multer');

var app = express();
var upload = multer({dest: 'upload/' });

app.post('/upload', upload.array('logo',2), function(req, res, next) {
	res.send({ret_code: '0'});
})

app.get('/form', function(req, res, next) {
	var form = fs.readFileSync('./form.html', {encoding:'utf8'});
	res.send(form);
	})

app.listen(3000);
```

form.html

```javascript
<form action="/upload" enctype="multipart/form-data" method="post">
	<h2>多图上传</h2>
	<input type="file" name="logo">
	<input type="file" name="logo">
	<input type="submit" value="提交">
</form>
```

## 获取上传图片的信息
***
```javascript
app.post('/upload', upload.single('logo'), function(req, res, next) {
	var file = req.file;
	console.log('文件类型:%s', file.mimetype);
	console.log('原始文件名:%s', file.originalname);
	console.log('文件大小:%s', file.size);
	console.log('文件保存路径:%s', file.path);
	})
```

## 自定义文件上传路径、名称
multer提供了storage这个参数来对资源保存的路径，文件名进行个性化设置。
使用注意事项如下：
* destination: 设置资源的保存路径。注意，如果没有这个配置项，默认会保存在/tmp/uploads下，此外路径需要自己创建。
* filename: 设置资源保存在本地的文件名.

```javascript
var createFolder = function(folder) {
	try {
		fs.accessSync(folder);
	} catch(e) {
		fs.mkdirSync（folder);
	}
};

var uploadFolder = './upload/';

createFolder(uploadFolder);

var storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, uploadFolder);  // 保存的路径，备注：需要自己创建
	},
	filename: function(req, file, cb) {
		// 将保存文件设置为字段名 + 时间戳
		cb(null, file.fieldname + '-' + Date.now());
	}
});

var upload = multer({ storage: storage });

app.post('/upload', upload.single('logo'), function(req, res, next) {
	var file = req.file;
	res.send({ status: '0'});
})
```
