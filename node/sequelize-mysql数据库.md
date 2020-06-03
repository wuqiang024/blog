## Nodejs + sequelize实现增删改查
***
* 安装
```javascript
cnpm install sequelize -S
cnpm install mysql2 -S  // cnpm install mysql提示不完整
```

* 创建数据库配置文件db.js配置数据库
```javascript
const Sequelize = require('sequelize');

module.exports = new Sequelize('blog', 'root', '123456', {
	host: 'localhost', // 数据库地址
	dialect: 'mysql', // 指定链接的数据库类型
	operatorsAliases: false,
	pool: {
		max: 5, // 连接池中最大连接数
		min: 0, // 连接池中最小连接数
		idle: 10000  // 如果一个线程10秒内没被使用过的话，那么释放线程
	}
});
```

* 数据库连接
```javascript
const db = require('./db');
db.authenticate().then(() => {
	console.log('connected');
}).catch((err) => {
	console.log(err);
})
```

* 创建一个model文件user.js
```javascript
const Sequelize = require('sequelize');
var db = require('./db');

// 创建model
var User = db.define('user', {
	id: {type: Sequelize.INTEGER, autoIncrement: true, primariKey: true, unique: true},
	userName: {type: Sequelize.STRING, field: 'user_name'},
	email: {type: Sequelize.STRING} // 没有指定field，表中键名与对象键名相同，为email
}, {
	// 如果为true则表的名称和model相同，即user
	// 为false MYSQL创建的表名称会是users
	// 如果指定的表名称本来就是复数则形式不变
	freezeTableName: true
});

User.sync({force: false}).then(function() {
	console.log('success to start');
}).catch(function(err) {
	console.log('failed to start');
})

// 创建表
// User.sync()会创建表并返回一个Promise对象
// 如果force = true则会把存在的表(如果users表已经存在)先销毁再创建表
// 默认情况下force = false
// var user = User.sync({force: false})
```

## sequelize 常用配置
***
```javascript
const Sequelize = require('sequelize');
const db = require('./db');
const User = db.define('user', {
	id: {
		type: Sequelize.INTEGER,
		field: 'id',
		primariKey: true,
		autoIncrement: true,
	},
	username: Sequelize.STRING,
	password: Sequelize.STRING,
	email: Sequelize.STRING,
	nickname: Sequelize.STRING,
	createdAt: {
		type: Sequelize.DATE,
		field: 'created_at'
	},
	updatedAt: {
		type: Sequelize.DATE,
		field: 'updated_at',
	},
}, {
	tableName: 'user', // 实例对应的表名
	timestamps: true, // 如果需要sequelize帮你维护createAt,updatedAt和deletedAt必须先启用timestamps功能
	createdAt: 'created_at', // 将createdAt对应到数据库的created_at字段
	updatedAt: 'updated_at', // 将updatedAt对应到数据库的updated_at字段
	deletedAt: false, // 删除数据时不删除数据，而是更新deletedAt字段，如果需要设置为true,则上面的deletedAt字段不能为false，也就是必须启用
	paranoid: false
})

module.exports = User;
```

## 添加新用户
***
```javascript
exports.addUser = function(username, email) {
	return User.create({
	userName: username,
	email: email
	}).then(function(result) {
		console.log('操作成功' + result);
	}).catch(function(err) {
		console.log('操作失败' + err);
	})
}
```

## 通过用户名查找用户
***
```javascript
exports.findByName = function(userName) {
	return User.findOne({where: {user_name: userName}}).then(function(result) {
		console.log(result.id);
	}).catch(function(err) {
		console.log('发生错误' + err);
	})
```

## 更新用户信息
***
```javascript
exports.updateUser = function(id) {
	return findOne({where: {id: id}}).then(function(user) {
		return user.update({email:'jack3@qq.com'}).then(function(result) {
			console.log(result);
		}).catch(function(err) {
			console.log(err);
		})
	})
}
```

## 删除用户
***
```javascript
exports.destroy = function(id) {
	return User.destroy({where: {id: id}}).then(function(result) {
		console.log('success');
	}).catch(function(err) {
		console.log(err);
	})
}
```

## 测试
***
```javascript
var user = require('./user');
user.findByName('jack');
user.addUser('jack2', 'jack@126.com');
user.update(1001);
user.destroy(1001);
```

## sequelize-cli的安装和使用
```javascript
cnpm install sequelize-cli -g
sequelize init
sequelize model:generate --name User --attributes firstName:string,lastName:string,email:string
```

