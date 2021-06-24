porcess是Node的全局模块，作用比较直观，可以通过它来获得node进程相关的信息，比如运行node程序时的命令行参数。或者设置进程相关信息，比如设置环境变量。

## 环境变量:process.env
使用频率很高，node服务运行时，时常会判断当前服务运行的环境
```
if(process.env.NODE_ENV == 'production') {
	console.log('生产环境');
} else {
	console.log('非生产环境');
}
```
运行命令 `NODE_ENV=production node env.js`

## 异步
使用频率很高，通常用在异步的场景

```javascript
console.log('海贼王');
process.nextTick(function() {
	console.log('火影忍者');
});
console.log('死神');
// 输出如下
// 海贼王
// 死神
// 火影忍者
```

process.nextTick(fn) 咋看跟setTimeout(fn, 0)很像，但实际上有着实现及性能上的差异。
* process.nextTick(fn) 将fn放到node事件循环的下一个tick里
* process.nextTick(fn) 比setTimeout(fn, 0)性能高
* process.nextTick()会把任务放在当前事件循环队列的队尾，而setImmediate()会把任务放在下一个队列的对首，setTimeout()会把任务放在他两中间

## 获取命令行参数： process.argv
process.argv返回一个数组，数组元素分布如下
* 元素1: node
* 元素2: 可执行文件的绝对路径
* 元素x: 其他，比如参数等

```javascript
// print process.argv
process.argv.forEach(function(val, index, array) {
	console.log('参数' + index + ':' + val);
})
```

## 获得node specific参数：
跟process.argv很像，但差异很大，它会返回node specific的参数（也就是运行Node程序特有的参数，比如 --harmony).
这部分参数不会出现在process.argv里。
当输入 `node --harmony execArgv.js --nick chyingp`, execArgv.js代码如下

```javascript
process.execArgv.forEach(function(val, index, array) {
	console.log(index + ':' + val);
})
// 输出:
// 0: --harmony

process.argv.forEach(function(val, index, array) {
	console.log(index + ':' + val);
})
// 输出
// 0: /User/a/.nvm/versions/node/v6.1.0/bin/node
// 1: /Users/a/Documents/git-node/nodejs-learning-guide/examples/execArgv.js
// 2: --nick
// 3: chyinp
```

## 当前工作路径: process.cwd()  process.chdir(directory)
* process.cwd() 返回当前工作路径
* process.chdir(directory): 切换当前工作路径


## IPC相关
* process.connected: 如果当前进程是子进程，而且与父进程之间通过IPC通道连接着，则为true;
* process.disconnect(): 断开与父进程之间的IPC通道，此时会将process.connected设置为false;

```javascript
var child_process = require('child_process');

child_process.fork('./connectedChild.js', {
  stdio: 'inherit'
});
```

然后，在 connectedChild.js 里面。
```
console.log( 'process.connected: ' + process.connected );
process.disconnect();
console.log( 'process.connected: ' + process.connected );

// 输出：
// process.connected: true
// process.connected: false
```

## 标准输入/标准输出/标准错误输出: process.stdin, process.stdout, process.stderr
```
process.stdin.setEncoding('utf8');
process.stdin.on('readable', ()=> {
	var chunk = process.stdin.read();
	if(chunk !== null) {
		process.stdout.write(`data:${chunk}`);
	}
})

process.stdin.on('end', ()=> {
	process.stdout.write('end');
})
```

## 用户组/用户相关
process.seteuid(id)： process.geteuid()：获得当前用户的id。（POSIX平台上才有效）

process.getgid(id) process.getgid()：获得当前群组的id。（POSIX平台上才有效，群组、有效群组 的区别，请自行谷歌）

process.setegid(id) process.getegid()：获得当前有效群组的id。（POSIX平台上才有效）

process.setroups(groups)： process.getgroups()：获得附加群组的id。（POSIX平台上才有效，

process.setgroups(groups)： process.setgroups(groups)：

process.initgroups(user, extra_group)：


## 当前进程信息
* process.pid: 返回进程id
* process.title: 可以用它来修改进程的名字，当你用ps命令，同时有多个node进程在跑的时候，作用就出来了。


## 运行情况/资源占用情况
* process.uptime(): 当前node进程已经运行了多长时间(单位是秒)
* process.memoryUsage(): 返回进程占用的内城，单位是字节。输出内容大致如下
```
{
	rss: 19882999,
	heapTotal: 893938,  // v8占用的内存
	heapUsed: 424244  // v8实际使用了的内存
}
```

* process.cpuUsage()
cpu使用时间耗时，单位为毫秒。user表示用户代码运行占用时间，system表示系统占用时间。如果当前进程占用多个内核来执行任务，那么数值会比实际感知的要大。
```
const startUsage = process.cpuUsage();
// { user:38579, system: 6986}

// spin the CPU for 500 milliseconds
const now = Date.now();
while( Date.now() - now < 500);
console.log(process.cpuUsage(startUsage));
// { user:514883, system: 11226 }
```

* process.hrtime(): 一般用于做性能基准测试。返回一个数组

## node 可执行程序相关信息
1、process.version: 返回当前Node版本
2、process.versions: 返回node版本，以及依赖库的版本，如下
```
{
	http_parser: '2.7.0',
	node: '6.1.0'
}
```
3、process.release: 返回当前node发行版本的相关信息，大部分时间不会用到。
4、process.config: 返回当前node版本编译时的参数，很少会用到，一般用来查问题
5、process.execPath: node可执行程序的绝对路径，比如'/usr/local/bin/node'


## 进程运行所在环境
* process.arch: 返回当前系统的处理器架构（字符串)
* process.platform: 返回关于平台描述的字符串


## process.kill(pid, signal)
process.kill()这个方法可能会让初学者感到困惑，其实他不是用来杀死进程的，而是用来向进程发送信号。
```
console.log('hello');
process.kill(process.pid, 'SIGHUP');
console.log('world');
```
可以看到最后一行没有执行，因为向当前进程发送SIGHUP信号，进程退出所致。
可以通过监听SIGHUP事件，来阻止它的默认行为。
```
process.on('SIGHUP', ()=>{
	console.log('test')
})
```

## 终止进程: process.exit(),  process.exitCode
1、process.exit(exitCode)可以用来立即退出进程。
2、写数据到process.stdout后，立即调用process.exit()是不保险的，因为在node里面，往stdout写数据是非阻塞的，可以跨越多个事件循环。
于是，可能写到一半就跪了。比较保险的做法是，通过process.exitCode设置退出码，然后等进程自动退出。
3、如果程序出现异常，必须退出不可，那么可以抛出一个未被捕获的error,来终止进程，这个逼process.exit()安全
