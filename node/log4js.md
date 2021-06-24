log4js是使用比较多的一个日志组件，经常跟express一起使用。

## 入门例子
***
输出日志如下, 包括日志打印时间、日志级别、日志分类、日志内容

```
var log4js = require('log4js');
var logger = log4js.getLogger();
logger.debug('hello world');
// 输出
// [2017-02-29 21:28:22.853] [DEBUG] [default] - hello world
```

## 日志级别
***
logger.setLevel('INFO');表示想要打印的最低级别的日志是INFO，也就是说，调用类似logger.debug()等
级别低于INFO的接口，日志是不会打印出来的。

```
var log4js = require('log4js');
var logger = log4js.getLogger();
logger.setLevel('INFO');
```

## 日志级别
***
除级别外，还可以对日志进行分类，log4js.getLogger(category),如下所示

```
var log4js = require('log4js');
var alogger = log4js.getLogger('category-a');
var blogger = log4js.getLogger('category-b');

alogger.info('hello');
blogger.info('hello');
//输出日志如下
// [2017-02-28 22:36:57.570] [INFO] category-a - hello
// [2017-02-28 22:36:57.570] [INFO] category-b - hello
```

# appenders
***
appenders指定日志输出的位置，可以同时配置多个。用category划分，比如log4js.getLogger('info')应用的就是
type为dateFile的配置
可以注意到，type为console的配置没有声明category，因此，所有的日志都会打印到控制台。

```
var log4js = require('log4js');
log4js.configure({
	appenders:[
		{ type: 'console'},
		{ type: 'dateFile', filename: './logs/info.log', category: 'info' }
	]
});

var logger = log4js.getLogger('info');
logger.setLevel('INFO');
```

## express应用
***
一个比较简单的例子如下，日志全部打印到控制台

```
var express = require('express');
var log4js = require('log4js');
var app = express();

log4js.configure({
	appenders: [
		{ type: 'console', category: 'app' }
	]
});

var logger = log4js.getLogger('app');
logger.setLevel（‘INFO'）；
app.use(log4js.connectLogger(logger));
app.use(function(req, res, next) {
	res.send('ok');
});
app.listen(3000);
```

log4js.connectLogger(logger)时，可以声明日志的级别。

```
// 级别 > INFO 的日志才会被打印
logger.setLevel('INFO');

// 日志的级别是WARN
app.use(log4js.connectLogger(logger, {level: 'WARN'}));
```