# watch服务
```js
const fs = require('fs');
const exec = require('child_process').exec;

function watch() {
	const child = exec('node server.js');
	const watcher = fs.watch(__dirname + '/server.js', function() {
		console.log('File changed, reloading');
		child.kill();
		watcher.close();
		watch()
	})
}

watch();
```