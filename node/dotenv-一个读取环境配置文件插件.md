## 安装
***

`npm install dotenv`  或者 `yarn add dotenv`


## 用法
***

尽可能早的在你的应用中加载配置dotenv插件

`require('dotenv').config()`

在应用根目录下创建一个 .env 文件， 通过 NAME=VALUE的方式添加一些环境变量。例如:

```
DB_HOST=localhost
DB_USER=root
DB_PASS=slmp13
```

现在process.env中就会包含你定义在.env文件中的键值对

```
const db = require('db');
db.connect({
	host: process.env.DB_HOST,
	username: process.env.DB_USER,
	password: process.env.DB_PASS
})
```