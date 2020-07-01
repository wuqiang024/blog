# javascript多线程编程
***
浏览器端的javascript是以单线程的方式执行的，也就是说javascript和UI渲染占用同一个主线程，那就意味着，如果JavaScript进行高负载的数据处理，UI渲染就很有可能被阻断，浏览器就会出现卡顿，降低用户体验。

为此，JavaScript提供了异步操作，比如定时器(setTimeout,setInterval)事件，ajax请求，I/O回调等。我们可以把高负载的任务用异步处理，他们会被放入浏览器的事件任务队列(event loop)中去，等到javascript运行时执行线程空闲的时候，事件队列才会按照先进先出的原则被一一执行。

通过类似定时器，回调函数等异步编程方式在平常的工作中已经足够，但是如果做复杂运算，这种方式的不足就逐渐体现出来，比如setTimeout拿到的值并不准确，或者页面有复杂运算的时候很容易触发假死状态，异步代码会影响主线程的代码执行，异步终究还是单线程，不能从根本上解决问题。

多线程(Web Worker)就应运而生，他是HTML5标准的一部分，这个规范定义了一套API，允许一段JS程序运行在主线程之外的另一个线程中。将一些任务分配给后者运行，在主线程运行的同时，Worker(子)线程在后台运行，两者互不干扰，等到Worker线程完成计算任务，再把结果返回给主线程。这样的好处是，一些计算密集型或高延迟任务，被Worker线程负担了，主线程(通常负责UI交互)就会很流畅，不会被阻塞或拖慢。

`什么是Web Worker`

![https://ask.qcloudimg.com/http-save/1069749/6vqxgh4sk9.jpeg?imageView2/2/w/1620](https://ask.qcloudimg.com/http-save/1069749/6vqxgh4sk9.jpeg?imageView2/2/w/1620)

worker是Window对象的一个方法，就是用它来创建多线程。可以通过以下方式来检测你的浏览器是否支持Worker。
```js
if(window.Worker) { ... your code ... }
```

一个worker是使用一个构造函数Worker创建的对象，这个构造函数需要传入一个JavaScript文件，这个文件包含将在工作线程中运行的代码。类似于这样:
```js
let myWorker = new Worker('worker.js');
```

主线程和子线程的数据是不共享的，worker通过postMessage()方法和onmessage事件进行数据通信。主线程和子线程是双向的，都可以发送和监听事件。向一个worker发送消息需要这样做(main.js):
```js
    myWorker.postMessage('hello'); // 发送
    worker.onmessage = function(event) {
        console.log(event.data);
        doSomething();
    }
```

postMessage所传的数据都是拷贝传递(ArrayBuffer类型除外),所以子线程也是类似传递(work.js)
```js
addEventListener('message', function(e) {
    postMessage(e.data);
}, false)
```

当子线程运行结束后，使用完毕，为了节省系统资源，可以手动关闭子线程。如果worker没有监听消息，那么当所有任务执行完毕后(包括计算器)，他会自动关闭。
```js
// 在主线程中关闭
worker.terminate()
// 在子线程里关闭
close()
```

worker也提供了错误处理机制，当出错时会触发error事件。
```js
// 监听error事件
worker.addEventListener('error', function(e) {
    console.log(e);
})
```
web worker本身很简单，但是他的限制特别多。

## 使用的问题
***
`1、同源限制`
分配给Worker线程运行的脚本文件(worker.js)，必须与主线程的脚本文件(main.js)同源。这里的同源限制包括协议，域名，端口号，不支持本地地址(file://)。这会带来一个问题，我们经常使用CDN来存储JS文件，主线程的worker.js的域名指的是html所在的域，通过new Worker(url)加载的url属于CDN的域，会带来跨域的问题，实际开发中我们不会把所有的代码都放到一个文件中让子线程加载，肯定会选择模块化开发。通过工具或库把代码合并到一个文件中，然后把子线程的代码生成一个文件url。解决方法。
* 将动态生成的脚本转成Blob对象
* 然后给这个Blob对象创建一个URL
* 最后将这个创建好的URL作为地址传给Worker的构造函数

```js
let script = 'console.log("hello world")';
let workerBlob = new Blob([script], {type:'text/javascript'});
let url = URL.createObjectURL(workerBlob);
let worker = new Worker(url);
```

`2、访问限制`
Worker子线程所在的全局对象，与主线程不在同一个上下文环境，无法读取主线程所在网页的DOM对象，也无法使用document,window,parent这些对象，global对象的指向有变更，window需要改写成self，不能执行alert()方法和confirm()方法，只能读取部分navigator对象内的数据。另外chrome的console.log(倒是可以使用)，也支持debugger断点，增加调试的便利性。

`3、使用异步Worker子线程可以使用XMLHttpRequest对象发出ajax请求，可以使用setTimeout,setInterval方法，也可以使用websocket进行持续连接，也可以通过importScripts(url)加载另外的脚本文件，但是仍然不能跨域。

### 应用场景
***
1、使用专用线程进行数学运算
Web Worker设计的初衷是用来做计算耗时任务，大数据的处理，而这种计算放在worker中并不会中断前端用户的操作，避免代码卡顿带来不必要的用户体验。例如处理ajax返回的大批量数据，读取用户上传文件，计算MD5,canvas的位图的过滤，分析视频和声频文件等。worker中除了缺失了BOM和DOM操作能力外，还是拥有非常强大的js逻辑运算处理能力的，相当于nodejs一个级别的运行环境。
2、高频的用户交互
高频的用户交互适用于根据用户的输入习惯，历史记录，以及缓存等信息来协助用户完成输入的纠错，校正功能等类似场景，用户频繁输入的响应处理同样可以考虑放在web worker中执行。例如，我们可以做一个像word一样的应用，当用户打字时，后台立即在词典中进行查找，帮助用户进行纠错。
3、数据的预取
对于一些有大量数据的前后台交互产品，可以新开一个线程专门用来进行数据的预取和缓冲数据，worker可以用在本地web数据库的行写入和更改，长时间持续的运行，不会被主线程的活动打断，也有利于随时响应主线程的通信，可以配合XMLHttpRequest和websocket进行不断开的通信，实现守卫进程。

## 小结
***
对于Web Worker这项新技术，无论在PC还是移动端，都很实用，腾讯新闻前端组进行了广泛的尝试。Web Worker的实现为前端程序带来了后台计算的能力，实现了主UI线程与复杂计算线程的分离。从而极大减轻了因计算量大而造成UI阻塞而出现的页面卡顿，并更大程度的利用了终端硬件的性能。他目前最大的问题在于不兼容IE9，在兼容性要求不是那么严格的地方，尽可能的使用吧。