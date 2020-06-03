## querystring: 可以用作通用解析器的模块
***
很多时候我们会从数据库或其他地方得到这种奇怪格式的字符串:
name:Shpie;shape:fox;condition:new，一般来说我们会利用字符串切割的方式来将字符串划分到JS对象中。
不过querystring也是个现成的工具。

```
const str = `name:sophie;shape:fox;condition:new`;
const result = querystring.parse(str, ';', ':');
```

## V8 Inspector
***
以`--inspect`运行你的Node应用程序，他会反馈你某个URL。将该URL复制到chrome中并打开，你就可以使用chrome DevTools来调试你的Node应用程序。


## Server.listen 可以使用Object作为参数
***
我更喜欢命名参数的方式调用函数，这样相较于按照顺序的无命名参数会更加直观。别忘了Server.listen也可以使用某个Object作为参数。

```
const http = require('http');
http.createServer().listen({
	port: 8000,
	host: 'localhost'
})
```

## 相对地址
***
你传入fs模块的距离可以使相对地址，即相对于porcess.cwd()。

```
const fs = require('fs');
const path = require('path');
fs.readFile(path.join(__dirname, 'myFile.txt'), (err, data)=>{
	// do something
})
```

## Path Parsing: 路径解析
***
之前我不知道的某个功能就是从某个文件名中解析出路径，文件名，文件扩展等:

```
let filePath = '/someDir/someFile.json';
path.parse(filePath).base = 'someFile.json';
path.parse(filePath).name = 'someFile';
path.parse(filePath).ext = '.json'
```

## Logging with colors
***
别忘了console.dir(obj, {colors: true})能够以不同的色彩打印出键和值，这一点会大大增加日志的可读性。


## 用setInterval执行定时任务
***
我喜欢用setInterval 来定期执行数据库清理任务，不过默认情况下在存在setInterval的时候，NodeJS并不会退出，你可以使用
如下方法让NodeJs沉睡。

```
const dailyCleanup = setInterval(()=>{
	cleanup();
}, 1000*60*60*24);
dailyCleanup.unref();
```

## Use Signal Constants
***
如果你尝试在NodeJs中杀死某个进程，估计你用过如下语法:

```
process.kill(process.pid, 'SIGTERM');
```
这个没啥问题，不过既然第二个参数能够同时使用字符串和整形变量，那么还不如使用全局变量:

```
process.kill(process.pik, os.constants.signals.SIGTERM);
```

## IP Address Validation
***
NodeJS中含有内置的IP地址检验工具，可以免得你写额外的正则表达式。

```
require('net').isIP('10.0.0.1') // 返回4
require('net').isIP('cats')  // 返回0
```

## os.EOF
***
NodeJS内置了os.EOF,其在windows下是rn, 在其他地方是n,使用os.EOF能够让你的代码在不同操作系统上保证一致性。


## HTTP状态码
***
NodeJS帮我们内置了HTTP状态码及其描述，也就是http.STATUS_CODES，键为状态值，值为描述
你可以按照如下方法使用:

```
res.code === 301 // true
http.STATUS_CODES[res.code] === 'Moved Permanently';
```

## 避免异常崩溃
***
有时候碰到如下这种导致服务器崩溃的情况还是挺无奈的：

```
const jsonData = getDataFromApi();  // bad data
const data = JSON.parse(jsonData);
```
为了避免这种情况，在全局加上了一个:

```
process.on('uncaughtException', console.error);
```
当然这种办法不是最佳实践。如果在大型项目中还是用PM2，然后将所有可能崩溃的代码加入到`try...catch`中。


## Just this once()
***
除了`on`方法，`once`方法也适用于所有的EventEmitters。

```
server.once('request', (req, res)=>{});
```

## Custom Console
***
你可以使用 new console.Console(stdout, errout), 然后设置自定义的输出流。你可以选择创建console将数据输出到文件或者socket或者第三方中。


## DNS lookup
***
略


## fs在不同OS上有一定差异
***
* fs.stats()返回的对象中的mode属性在windows和其他系统中存在差异
* fs.lchmod()仅在macos中有效
* 仅在windows中支持调用fs.symlink()时使用type参数
* 仅仅在macOS与Windows中调用fs.watch()时传入recursive选项
* 在linux和Windows中fs.watch()的回调可以传入某个文件名
* 使用fs.open()以及 a+ 属性打开某个目录时仅仅在FreeBSD以及Windows上起作用，在macOS以及linux上存在问题
* 在Linux下以追加模式打开某个文件时，传入到fs.write()的position参数会被忽略。


## net模块差不多比http快上两倍
***
笔者在文档中看到一些关于二者性能的讨论，还特地运行了两个服务器来进行真实比较。结果来看http.Server大概每秒可以接入3400个请求，而net.Server可以接入大概5500个请求。

```
const net = require(`net`);
const http = require(`http`);

function parseIncomingMessage(res) {
  return new Promise((resolve) => {
    let data = ``;

    res.on(`data`, (chunk) => {
      data += chunk;
    });

    res.on(`end`, () => resolve(data));
  });
}

const testLimit = 5000;


/*  ------------------  */
/*  --  NET client  --  */
/*  ------------------  */
function testNetClient() {
  const netTest = {
    startTime: process.hrtime(),
    responseCount: 0,
    testCount: 0,
    payloadData: {
      type: `millipede`,
      feet: 100,
      test: 0,
    },
  };

  function handleSocketConnect() {
    netTest.payloadData.test++;
    netTest.payloadData.feet++;

    const payload = JSON.stringify(netTest.payloadData);

    this.end(payload, `utf8`);
  }

  function handleSocketData() {
    netTest.responseCount++;

    if (netTest.responseCount === testLimit) {
      const hrDiff = process.hrtime(netTest.startTime);
      const elapsedTime = hrDiff[0] * 1e3 + hrDiff[1] / 1e6;
      const requestsPerSecond = (testLimit / (elapsedTime / 1000)).toLocaleString();

      console.info(`net.Server handled an average of ${requestsPerSecond} requests per second.`);
    }
  }

  while (netTest.testCount < testLimit) {
    netTest.testCount++;
    const socket = net.connect(8888, handleSocketConnect);
    socket.on(`data`, handleSocketData);
  }
}


/*  -------------------  */
/*  --  HTTP client  --  */
/*  -------------------  */
function testHttpClient() {
  const httpTest = {
    startTime: process.hrtime(),
    responseCount: 0,
    testCount: 0,
  };

  const payloadData = {
    type: `centipede`,
    feet: 100,
    test: 0,
  };

  const options = {
    hostname: `localhost`,
    port: 8080,
    method: `POST`,
    headers: {
      'Content-Type': `application/x-www-form-urlencoded`,
    },
  };

  function handleResponse(res) {
    parseIncomingMessage(res).then(() => {
      httpTest.responseCount++;

      if (httpTest.responseCount === testLimit) {
        const hrDiff = process.hrtime(httpTest.startTime);
        const elapsedTime = hrDiff[0] * 1e3 + hrDiff[1] / 1e6;
        const requestsPerSecond = (testLimit / (elapsedTime / 1000)).toLocaleString();

        console.info(`http.Server handled an average of ${requestsPerSecond} requests per second.`);
      }
    });
  }

  while (httpTest.testCount < testLimit) {
    httpTest.testCount++;
    payloadData.test = httpTest.testCount;
    payloadData.feet++;

    const payload = JSON.stringify(payloadData);

    options[`Content-Length`] = Buffer.byteLength(payload);

    const req = http.request(options, handleResponse);
    req.end(payload);
  }
}

/*  --  Start tests  --  */
// flip these occasionally to ensure there's no bias based on order
setTimeout(() => {
  console.info(`Starting testNetClient()`);
  testNetClient();
}, 50);

setTimeout(() => {
  console.info(`Starting testHttpClient()`);
  testHttpClient();
}, 2000);
```

```
const net = require(`net`);
const http = require(`http`);

function renderAnimalString(jsonString) {
  const data = JSON.parse(jsonString);
  return `${data.test}: your are a ${data.type} and you have ${data.feet} feet.`;
}


/*  ------------------  */
/*  --  NET server  --  */
/*  ------------------  */

net
  .createServer((socket) => {
    socket.on(`data`, (jsonString) => {
      socket.end(renderAnimalString(jsonString));
    });
  })
  .listen(8888);


/*  -------------------  */
/*  --  HTTP server  --  */
/*  -------------------  */

function parseIncomingMessage(res) {
  return new Promise((resolve) => {
    let data = ``;

    res.on(`data`, (chunk) => {
      data += chunk;
    });

    res.on(`end`, () => resolve(data));
  });
}

http
  .createServer()
  .listen(8080)
  .on(`request`, (req, res) => {
    parseIncomingMessage(req).then((jsonString) => {
      res.end(renderAnimalString(jsonString));
    });
  });
```
