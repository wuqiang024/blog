## UEditor
***
UEditor官方支持的版本有PHP,JSP,ASP.NET,ueditor for nodejs可以让你的UEditor支持nodejs

```javascript
cnpm install ueditor -S
```

## Usage
```javascript
var bodyParser = require('body-parser');
var ueditor = require('ueditor');
app.use(bodyParser.urlencoded({
	extended: true
}));
app.use(bodyParser.json());

app.use('/ueditor/ue', ueditor(path.join(__dirname,'public'), function(req, res, next) {
	if(req.query.action === 'uploadimage') {
		// 这里可以获取上传图片的信息
		var foo = req.ueditor;
		console.log(foo.filename);
		console.log(foo.encoding);
		console.log(foo.mimetype);
		// 下面填写你要把图片保存到的路径，以(path.join(__dirname, 'public'))作为根路径。
		var img_url = 'yourpath';
		res.ue_up(img_url);
	} else if(req.query.action === 'listimage') {
		var dir_url = 'you img_dir';  // 要展示给客户端的文件夹路径
		res.ue_list(dir_url) // 客户端会列出dir_url目录下的所有图片
	} else {
		res.setHeader('Content-type', 'application/json');
		// 这里填写ueditor.config.json这个文件的路径
		res.redirect('/ueditor/ueditor.config.json');
	}
}))
```

## 七牛上传
***
```javascript
...
app.use('/ueditor/ue', ueditor(path.join(__dirname, 'public'), {
	qn: {
		accessKey: 'your accessKey',
		secretKey: 'your secretKey',
		bucket: 'your bucket name',
		origin: 'http://{bucket}.u.qiniudn.com'
	}
}, function(req, res, next) {
	var imgDir = '/img/ueditor';
	if(req.query.action === 'uploadimage') {
		var foo = req.ueditor;
		var imgname = req.ueditor.filename;
		res.ue_up(imgDir);  // 你只要输入要保存的地址，保存操作交给ueditor
	} else if(req.query.action === 'listimage') {
		res.ue_list(imgDir);
	} else {
		res.setHeader('Content-type', 'application/json');
		res.redirect('/ueditor/ueditor.config.json')
	}
}))

## 上传配置
```javascript
app.use('/ueditor/ue', static_url, config={}, callback);
```
当config为空时，会默认把图片上传到static_url _ '/img/ueditor'目录下。
比如例子Usage中图片会上传到项目的public/img/ueditor目录。
当配置了config.qn图片则会只上传到七牛服务器而不会上传到项目目录。
同时上传到七牛和项目目录只需配置config.local即可。

```javascript
config = {
	qn: {...},
	local: true
}
```

## 多类型文件上传(附件，视频，图片)
***
```javascript
...
app.use('/ueditor/ue', ueditor(path.join(__dirname, 'public'), function(req, res, next) {
	var imgDir = '/img/ueditor';
	var ActionType = req.query.action;
	if(ActionType === 'uploadimage' || ActionType === 'uploadfile' || ActionType === 'uploadvideo') {
		var file_url = imgDir;
		if(ActionType === 'uploadfile') {
			file_url = '/file/ueditor';
		}
		if(ActionType === 'uploadvideo') {
			file_url = '/video/ueditor';
		}
		res.ue_up(file_url);
		res.setHeader('Content-type', 'text/html');
	} else if(ActionType === 'listimage') {
		res.ue_list(imgDir);
	} else {
		res.setHeader('Content-type', 'application/json');
		res.redirect('/ueditor/ueditor.config.json');
	}
}))