不管是小项目还是大项目，将配置与代码分离是一个非常好的做法。我们通常将配置写到一个配置文件里，如config.js或config.json，并放到项目的根目录下。但实际开发的时候我们会有许多环境，如本地开发环境、测试环境和线上环境等，不同环境的配置不同，我们不可能每次部署时都要去修改引用config.test.js或者config.production.js。config-lite模块正是你需要的。

## config-lite
### 安装
```sh
cnpm i config-lite -S
```

### 版本迁移
在版本1里:
```js
const config = require('config-lite');
```

在版本2里: 你需要明确 config_basedir 目录用于冒泡查询config文件
```js
const config = require('config-lite')(__dirname);

const config = require('config-lite')({
	filename: 'test',
	config_basedir: __dirname,
	config_dir: 'config'
});
```

### 优先级
environment option > custom option > defalut option

例如:
```sh
$ NODE_ENV=test NODE_CONFIG='{"port":3000}' node app.js --port=3001
```

### 环境变量对应关系
* NODE_ENV -> filename
* CONFIG_BASEDIR || NODE_CONFIG_BASEDIR -> config_dirname
* CONFIG_DIR || NODE_CONFIG_DIR -> config_dir
* CONFIG || NODE_CONFIG -> onfig

加载顺序:
--port=3001 > NODE_CONFIG='{"port":3000}' > opt.config > test config file > defalut config file


***
config-lite是一个轻量级的读取配置文件的模块。config-lite会根据环境变量(NODE_ENV)的不同加载config目录下不同的配置文件。如果不设置NODE_ENV，则读取默认的defaut配置文件，如果设置了NODE_ENV，则会合并指定的配置文件和default配置文件作为配置，config-lite支持.js、.json、.node、.yml、.yaml后缀的文件。

如果程序以	`NODE_ENV=test node app`启动，则config-lite会依次降级查找config/test.js, config/test.json, config/test.node等等，并合并default配置；如果程序以`NODE_ENV=production node app`启动，则会依次会降级查找config/production.js等，并合并default配置。

config-lite还支持冒泡查找，即从传入的路径开始，从该目录不断往上一级目录查找config目录，直到找到或者到达根目录为止。

`config/defalut.js || config/test.js || confit/prod.js`
```javascript
module.exports = {
	port: 3000,
	session: {},
	mongodb: ''
}
```

配置说明：
1、port: 程序启动监听的端口号
2、session: express-session的配置信息
3、mongodb: mongodb的地址，以mongodb://协议开头