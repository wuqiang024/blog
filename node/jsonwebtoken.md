## Token
***
在计算机身份认证中是令牌(临时)的意思，在词法分析中是标记的意思。

## Token的特点
***
1、随机性
2、不可预测性
3、时效性
4、无状态、可扩展
5、跨域

## 基于Token的验证场景
***
1、客户端使用用户名和密码请求登录
2、服务端收到请求，验证登录是否成功
3、验证成功后，服务端会返回一个Token给客户端，反之，返回身份验证失败的信息
4、客户端收到Token后把Token用一种方式(cookie/localstorage/sessionstorage)储存起来
5、客户端每次发起请求时都将Token发给服务器
6、服务端收到请求后，验证Token的合法性，合法就返回客户端所需要的数据，反之返回验证失败的信息

## Token身份验证实现--jsonwebtoken
***
先安装第三方模块jsonwebtoken`cnpm install jsonwebtoken`

```javascript
const express = require('express');
const path = require('path');
const app = express();
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');

app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, '/')));

app.all('*', function(req, res, next) {
	res.header('Access-Control-Allow-Origin', '*');
	res.header('Access-Control-Allow-Headers', 'Content-Type,Content-Length,Auth,Accept,X-Requested-With');
	res.header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS');
	res.header('X-Powered-By', '3.1.2');
	if(req.method=='OPTIONS' {
		res.sendStatus(200); 让options请求快速返回
	}) else {
		next();
	}
})

app.get('/createToken', function(req, res) => {
	let user = {
		username: 'admin'
	}

	let secret = 'dktoken';
	let token = jwt.sign(user, secret, {
		'expiresIn': 60*60*24  // 设置过期时间，24小时
	})
	res.send({status: true, token})
})

app.post('/verifyToken', function(req, res) {
	let secret = 'dktoken';
	let token = request.headers['auth'];
	if(!token) {
		res.send({status: false, message: 'token不能为空'})
	}
	jwt.verify(token, secret, function(error, result) {
		if(error) {
			res.send({status: false})
		} else {
			res.send({status: true, data: result})
		}
	})
})

app.listen(8888);
```

## 前端ajax请求在请求头中包含Token
***
### ajax请求之jquery篇
```javascript
$.ajax({
	url: 'verifyToken',
	type: 'post',
	headers: {'auth': token},
	success: function(res) {
		console.log(res)
	}
})
```

### ajax请求之XMLHttpRequest篇
```javascript
var xhr = new XMLHttpRequest();
xhr.open('POST', 'verifyToken');
xhr.setRequestHeader('auth', token);
xhr.send();
```

### ajax请求之axios篇
```javascript
import axios from 'axios';
axios({
	url: url,
	params: _params || {},
	headers: { auth: token },
}).then(res => {
	if(!res.data.status && res.data.error == 'unauthorized') {
		router.push('login');
		return false;
	}
	resolve(res);
}).catch(error => {
	reject(error);
})
```

### ajax 请求之 superagent 篇
```javascript
import http from 'superagent'
http.post(getUrl(path))
    .set('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    .set('auth',  window.localStorage.getItem('access_token'))
    .end((err, res) => {});
```