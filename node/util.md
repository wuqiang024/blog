## debuglog(section)
***
很有用的调试方法。可以通过util.debuglog(name)来创建一个调试fn,这个fn的特点是，只有在运行程序的时候，声明环境变量NODE_DEBUG=name，
才会打印出调试信息。

可以看下面例子，直接运行`node debuglog.js`，没有任何输出。需要NODE_DEBUG=foo,才会有打印信息。

```javascript
var util = require('util');
var logger = util.debuglog('foo');
logger('hello');
```

如下所示，注意，6379是当前进程id。

```bash
NODE_DEBUG = foo  node debuglog.js
FOO 6379: hello world
```

此外，还以一次指定多个name, 通过逗号分隔。

```javascript
var util = require('util');
var firstLogger = util.debuglog('first');
var secontLogger = util.debuglog('second');

firstLogger('first');
secontLogger('second');
```

运行如下:

```bash
NODE_DEBUG = first,second node debuglog.js
```

## 将方法标志为作废：util.deprecate(fn, str)
***

将fn包裹一层，并返回一个新的函数fn2。调用fn2时，同样完成fn原有的功能，但同时会打印出错误日志，提示方法已作废，具体的提示信息就是第二个参数str。

```javascript
var util = require('util');
var foo = function() {
	console.log('foo');
};

var foo2 = util.deprecate(foo, 'foo is deprecate');

foo2();
```

如果嫌错误提示信息烦人，可以通过 --no-deprecation 参数禁掉。

```bash
node --no-deprecation deprecate.js
```


### 格式化打印：util.format()
***

```bash
util.format(hello %s', 'world');
```


### 调试方法: util.inspect(obj[, options]);
***

非常实用的一个方法，参数说明如下:

* obj: js原始值，或者对象。
* options: 配置参数，包含下面选项
** showHidden: 如果是true的话，obj的非枚举属性也会被展示出来。默认是false。
** depth: 如果Obj是对象，那么depth限制对象展示的层级，这对可读性有一定好处。默认是2.如果设置为null，则不做限制。
** colors: 自定义配色方案。
** showProxy:
** maxArrayLength: 如果obj是数组，那么限制最大可展示的数组个数，默认是100，如果设置为null,则不做限制，如果设置为0或者负数，则一个都不展示。


## util模块
***
1、util.promisify(fn)
2、util.inherits(child, parent)
3、util.isArray([]), util.isString()