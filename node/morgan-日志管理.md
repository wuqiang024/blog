```
npm install -S morgan
```

## 使用
***
使用配置非常简单，就两行代码。

```
var express = require('express');
var morgan = require('morgan');
var app = express();
app.use(morgan('combined'));

app.get('/', function(req, res) {
	res.send('test');
});

app.listen(3000);
```

运行服务，在浏览器里启动，就可以在控制台看到日志。

## 把日志写入到文件
***

```
var fs = require('fs');
var accessLogStream = fs.createWriteStream(path.join(__dirname, 'access.log'), {flag: 'a'});
app.use(morgan('combined', {stream: accessLogStream}));
```