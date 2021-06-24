## 安装session相关的包

```bash
npm install cookie-parse -S
npm install express-session -S
npm install session-file-store -S
```

## session相关配置

```javascript
var express = require('express');
var cookieParse = require('cookie-parse');
var session = require('express-session');
var fileStore = require('express-file-store')(session);
var identityKey = 'skey';
app.use(session({
	name: indentityKey,
	secret: 'chyingp',   // 用来对session id相关的cookie进行签名
	store: new FileStore(),  // 本地存储session(文本文件，也可以选择其他store,比如redis)
	saveUninitialized: false,  // 是否自动保存未初始化的会话，建议false
	resave: false,  // 是否每次都重新保存会话，建议false
	cookie: {
		maxAge: 10 * 1000  // 有效期，单位毫秒
	}
}))
```

## express-session的常用参数
***

* secret: 一个String类型的字符串，作为服务器端生成session的签名。
* name: 返回客户端的key的名称，默认为connect.sid，也可以自己设置。
* resave: 强制保存session即使它并没有变化，默认为true,建议设置成false。
* saveUninitialized: 强制将未初始化的session存储。当新建了一个session并且未设定属性或值时，它就处于未初始化状态。在设定一个cookie前，这对于登录验证，减轻服务端存储压力，权限控制是有帮助的。默认为true。建议手动添加。
* cookie: 设置返回到前端key的属性，默认值为 {path: '/', httpOnly: true, secure: false, maxAge: null}
* rolling: 在每次请求时强行设置cookie，这将重置cookie过期时间（默认：false)

```javascript
app.use(session({
	secret: 'nodesite',
	name: 'name',
	cookie: {maxAge: 60000},   // 过期时间, 设置过期时间比如是30分钟，只要浏览页面，30分钟没有操作的话再过期
	// secure https这样的情况才可以访问cookie
	resave: false,
	saveUninitialized: true  // 在每次请求时强行设置cookie， 这将重置cookie过期时间
}))
```

## express-session的常用方法
***

```javascript
req.session.destroy(function(er) {});
req.session.username = '张三';
req.session.username;  // 获取session
req.session.cookie.maxAge = 0;  // 设置cookie过期时间
```

## 负载均衡配置session, 把session保存到数据库里
***

使用redis存储session的好处在于
1、多进程session可以共存
2、网站重启session依旧在

```javascript
var express = require('express');
var session = require('express-session');
var RedisStore = require('connect-redis')(session);
var app = express();

// 设置cookie过期时间
app.use(cookieParse('nodesite'));

// 设置session
app.use(session({
	store: new RedisStore({
		host: '129.168.0.1',
		port: 6379,
		db: 'test_session',
		pass: '19819895'
	}),
	secret: 'nodesite',
	resave: false,
	saveUninitialized: true
}))
```

## cookie和redis的区别
***

1、cookie数据存在客户的浏览器上，session数据放在服务器上
2、cookie不是很安全，别人可以分析存在本地的cookie并进行cookie欺骗，考虑到安全应该使用session
3、session会在一定时间内保存在服务器上，当访问增多，会比较占用服务器的性能，考虑到减轻服务器性能方面，应当使用cookie。
4、单个cookie保存的数据不超过4K，很多浏览器都限制一个站点最多保存20个cookie。