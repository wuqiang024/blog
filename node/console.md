console模块提供了基础的调试功能，使用很简单，常用的API主要有console.log(), console.error()。
此外，可以基于Console类，方便的扩展出自己的console实例，比如把调试信息打印到文件里。而部署输出在控制台上。

## 基础例子
***
* console.log(msg): 普通打印日志
* console.error(msg): 错误日志打印
* console.info(msg): 等同于console.log(msg)
* console.warn(msg): 等同于console.error(msg)

## 自定义stdout
可以通过`new console.Console(stdout, stderr)`来创建自定义的console实例，这个功能很实用。
比如你想讲调试信息打印到本地文件，可以如下实现。

```javascript
var fs = require('fs');
var file = fs.createWriteStream('./stdout.txt');
var logger = new console.Console(file, file);
logger.log('hello');
logger.log('world');
```
// 备注：内容输出到stdout.txt里而不是打印到控制台

## 计时
通过console.time(label)和console.timeEnd(label)，来打印两个时间点之间的时间差。单位是毫秒，例子如下。

```javascript
var timeLabel = 'hello';
console.log(timeLabel);
setTimeout(console.timeEnd, 1000, timeLabel);
// 输入输出：
// hello: 1005.505ms
``` 

## 断言
通过console.assert(value, message)进行断言。如果value不为true,那么抛出AssertionError异常，并中断程序执行。
如下代码所示。第二个断言报错，程序停止执行。

```javascript
console.assert(true, '1、right');
console.assert(false, '2、right', '2、wrong')
```
为了避免程序异常退出，需要对上面异常进行处理

```javascript
try {
	console.assert(false, 'error occurred');
} catch(e) {
	console.log(e.message);
}
```

## 打印错误栈: console.trace(msg)
将msg打印到标准错误输出流里，包含当前代码的位置和堆栈信息

```javascript
console.trace('trace is called');
```

## 深层打印
console.dir(obj)跟console.log(obj)差不多。
当obj层级比较深时，可以通过depth自定义打印的层级数，默认是2，这对调试很有帮助。

```javascript
console.dir(obj, {depth: 3})
```