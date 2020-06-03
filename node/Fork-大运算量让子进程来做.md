实际项目中，很多时候都会有这种情况:
某些功能是有大数据量运算的，或者进行很消耗资源的操作。
这种情况下，如果在主线程中处理，会严重影响主进程的整体性能。
合理的方法是:
把可能对主线程造成压力的工作量，放到子进程中去，让子进程去独立完成。

# Forking(分叉)
child_process有一个fork(分叉)方法，可以满足上面的想法:

```js
var cp = require('child_process');
cp.fork('/child');
```

# 和分叉的NodeJS模块进行通信
约定: 主进程标识为father,子进程标识为child。

father.js代码:

```js
var cp = require('child_process');
var child = cp.fork('./child');
child.on('message', function(msg) {
	console.log(msg);
})

child.send('msg from father');
```

代码解析:
1、创建子进程、向子进程发送一条信息
2、当收到子进程发来的信息时，输出消息

child.js代码:
```js
process.send('msg from child');

process.on('message', function(msg) {
	console.log(msg);
})
```

代码解析:
1、发送一条消息给进程
2、当收到父进程消息时，输出消息。

`node father.js`运行程序。可以看到父进程和子进程通信成功。
注:进程间发送数据的类型不会丢失，比如发送JSON值，收到的也是JSON值，不会变成字符串。
