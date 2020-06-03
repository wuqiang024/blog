## 为什么需要cookie-parser
***
在nodejs里，读取、设置cookie，可分别通过如下方式:
1、读取cookie：可以通过req.headers.cookie来获取HTTP请求携带的cookie。大概是类似下面的字符串。

```
uid=2323232; visit=3;
```

2、设置cookie: 通过Set-Cookie首部来达到设置cookie的目的。

```
res.setHeader('Set-Cookie', 'visit=3; Max-Age=60; Path="/"');
```

很明显，无论是读取还是分析cookie的值，都不够方便。
在express里，我们可以通过cookie-parser来方便的完成cookie的读写。


## cookie-parse中间件的使用
使用很简单
* 读取cookie值: req.cookies.visit
* 设置cookie值得: res.cookie('visit', 3)

```
app.get('/', function(req, res, next) {
	if(req.headers.cookie) {
		console.log(req.headers.cookie);
	}

	var visit = req.cookies.visit || 0;
	res.cookie('visit', ++visit, {maxAge: 60000}); // 设置cookie
	res.send(visit);
})
```