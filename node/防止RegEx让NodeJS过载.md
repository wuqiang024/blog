# 通过事件组织应用
```js
const express = require('express');
const app = express();
const emails = require('./emails');
const routes = require('./routes');

app.use(express.json());

app.post('/users', routes.users.create); // 设置路由创建用户

app.on('user:created', emails.welcome); // 监听创建成功事件，绑定email代码

module.exports = app;
```

```js
const User = require('./../models/user');

module.exports.create = function(req, res, next) {
	const user = new User(req.body);
	user.save(function(err) {
		if(err) return next(err);
		res.app.emit('user:created', user); // 当用户注册成功时触发创建用户事件
		res.send('User created');
	})
}
```