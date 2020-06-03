# 代码

```js
const express = require('express');
const session = require('express-session');
const app = express();

app.listen(3000, function(res) {
    console.log('listening');
})

app.use(session({
    secret: 'xxxx', // 建议用128个字符的随机字符串
    cookie: { maxAge: 60 * 1000 },
    name: 'session_id'
}));

app.get('/', function(req, res) {
    // 检查session中的isVisit字段
    // 如果存在则增加一次，否则为session设置isVisit字段，并初始化为1
    if(req.session.isVisit) {   
        res.end(`第${req.session.isVisit}次来此页面`);
    } else {
        req.session.isVisit = 1;
        res.send('欢迎第一次来这里');
    }
});
```

# Cookie
在HTTP协议中，制定了Cookie机制，用于实现客户端和服务器端的状态共享。
Cookie是解决了HTTP无效状态的有效手段，服务器可以设置(set-cookie)或读取cookie所包含的信息。
实现原理:
客户端第一次请求: 服务器端如果需要记录用户信息(就是用户需要存session如: $SESSION['username']='test'),才会在响应信息中返回Set-cookie响应头，如果没有存入用户信息，也就是没有session操作时，不会返回Set-Cookie响应头，当然再次访问页面时，会在请求头中，带上cookie。

# session存入redis(持久化存储)
connect-redis是一个redis版的session存储器，使用node_redis作为驱动。借助他即可在Express中启用redis来持久化你的Session.
`npm install connect-redis`

# 参数
* client 你可以复用现有的redis客户端对象，由redis.createClient()创建
* host 服务器名
* port redis服务器端口
* socket

## 可选参数
* ttl TTL过期时间
* disableTTL 禁用设置的TTL
* db 使用第几个数据库
* pass redis数据库的密码
* prefix 数据表前缀即schema,默认为'sess:'

```js
const express = require('express');
const app = express();
app.listen(5000, function(res) {
    console.log('listening');
});

const session = require('express-session');
const redis = require('redis');
const client = redis.createClient('6379', '127.0.0.1');
const RedisStore = require('connect-redis')(session);
app.use(session({
    secret: 'signkey',
    store: new RedisStore(client:client),
    resave: false,
    saveUninitialized: false,
    name: 'session_id',
}));

app.use(function(req, res, next) {
    if(!req.session) {
        return next(new Error('error'));
    }
    next();
});

app.get('/', function(req, res) {
    if(req.session.isVisit) {
        req.session.isVisit++;
        req.session.username = 'test';
        res.send('第' + req.session.isVisit + '次来此页面');
    } else {
        req.session.isVisit = 1;
        res.send('欢迎第一次来这里');
        console.log(req.session);
    }
})
```

这样session就会转移到redis数据库中，为什么可以保证持久化呢，因为express服务器突然重启时，用户仍然可以使用当前cookies里面sessionID，从数据库获取他的会话状态，做到会话不丢失，提高了网站的健壮性。