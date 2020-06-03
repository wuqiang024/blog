# 单线程只是针对主进程，I/O操作系统底层进行多线程调度。也就是他仅仅起到一个监听作用。

# 单线程并不是只开一个进程。

```js
const cluster = require('cluster');
const http = require('http');
const numCpus = require('os').cpus().length;

if(cluster.isMaster) {
	for(let i = 0; i < numCpus; i++) {
		cluster.fork();
	}

	cluster.on('exit', (worker, code, signal) => {
		console.log(`工作进程${worker.process.pid}已退出`)
	})
} else {
	http.createServer((req, res) => {
		res.writeHead(200);
		res.end('test');
	}).listen(8000)
}