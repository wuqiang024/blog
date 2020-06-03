# 支持黑名单的JWT
当使用JSON Web Token(例如，通过Passport.js)，默认情况下，没有任何机制可以从发出的令牌中撤销访问权限。一旦发现了一些恶意用户活动，只要他们持有有效的标记，就无法阻止他们访问系统。通过实现一个不受信任令牌的黑名单，并在每个请求上验证，来减轻此问题。

```js
const jwt = require('express-jwt');
const blacklist = require('express-jwt-blacklist');

app.use(jwt({
	secret: 'my-secret',
	isRevoked: blacklist.isRevoked
}));

app.get('/logout', function(req, res) {
	blacklist.revoke(req.user);
})
```

# express-jwt
## 作用是什么
express-jwt是nodejs的一个中间件，他来验证指定http请求的JsonWebTokens的有效性，如果有效就将JsonWebTokens的值设置到req.user里面，然后路由到相应的router。此模块允许您使用Node.js应用程序中的JWT令牌来验证HTTP请求。JWT通常用于保护API端点。

## express-jwt和jsonwebtoken是什么关系
express-jwt内部引用了jsonwebtoken，对其封装使用。在实际的项目中这两个都需要引用，他们两的定位不一样，jsonwebtoken是用来生成token给客户端，express-jwt是用来验证token的

## 如何使用
### 安装
`cnpm install express-jwt -S`

### 设置需要保护的API
```js
const expressJWT = require('express-jwt');
const secretOrPrivateKey = 'hello BigManing'; // 加密token 校验token时要用
app.use(expressJWT({
	secret: secretOrPrivateKey
}).unless({
	path:['/getToken']  // 除了这个地址，其他的URL都要验证
}));
```

### 校验token失败时的处理
```js
app.use(function(err, req, res, next) {
	if(err.name === 'UnauthorizedError') {
		res.status(401).send('invalid token');
	}
})
```

token过期时的err值
```js
{
	"name": 'UnauthorizedError',
	"message": 'jwt expired',
	"code": 'invalid_token',
	"status": 401,
	"inner": {
		"name": "TokenExpiredError",
		"message": 'jwt expired',
		"expiredAt": '2017-08-03 ...'
	}
}
```

token无效时的err值
```js
{
	"name": 'UnauthorizedError',
	"message": "invalid_token",
	"code": "invalid_token",
	"status": 401,
	"inner": {
		"name": "JsonWebTokenError",
		"message": "invalid signature"
	}
}
```

## 定义返回给客户端token的接口
```js
const jwt = require('jsonwebtoken');
app.get('/getToken', function(req, res, next) {
	res.json({
		resutl: 'ok',
		token: jwt.sign({
			name: 'BinMaing',
			data: '===',
		}, secretOrPrivateKey, {
			expiresIn: 60 * 1
		})
	})
});
```

## express-jwt 与 jsonwebtoken
express-jwt是对jsonwebtoken进行了封装，在验证策略方面做了很多扩展，如果你的验证策略比较简单，那么使用jsonwebtoken就够了。

```js
app.use(function(req, res, next) {
	// 定义不用token的api
	if(req.originalUrl.indexOf('/getToken') >= 0) {
		return next();
	}
	// 定义用token的api对其验证
	var token = req.body.token || req.query.token || req.headers['x-access-token'];
	jwt.verify(token, secretOrPrivateKey, function(err, decoded) {
		if(err) {
			res.send({
				success: false,
				message: 'error',
			});
			return;
		} else {
			req.username = decoded.username;
			req.orgname = decoded.orgName;
			logger.debug(util.format(...));
			return next();
		}
	})
})