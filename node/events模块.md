# events模块

事件模块在Node.js中有很多好处，但用法可以很简单。

* Node.js是单进程单线程应用程序，但是通过事件和回调支持并发，所以性能非常高
* Node.js每个API都是异步的，并作为一个独立线程运行，使用异步函数调用，并处理并发
* Node.js基本上所有的事件机制都是用设计模式中观察者模式实现。
* Node.js单线程类似进入一个while(true)的事件循环，直到没有事件观察者退出，每个异步事件都生成一个事件观察者，如果有事件发生就调用该回调函数。
* 用法
** 实例化一个事件实例`new events.EventEmitter()
** 在实例对象上定义事件 on(eventName, function() {})
** 通过`emit`方法触发事件 emit(eventName)


```js
const events = require('events');
const emitter = new events.EventEmitter();

emitter.on('connection', function() {
	console.log('连接成功');
	emitter.emit('data_received');
})

emitter.on('data_received', function() {
	console.log('数据接收成功');
})

emitter.emit('connection');
console.log('程序执行完毕')
```