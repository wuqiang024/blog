# websocket
* websocket是一种在单个TCP连接上进行全双工通信的协议，即连接双方可以同时收发数据，他可以在用户的浏览器和服务器之间打开双工，双向通讯会话。
* websocket API提供全局方法创建实例。

```js
// 必须传入绝对URL，可以是任何网站
const s = new WebSocket('ws://www.baidu.com');
s.readyState  // 0 建立链接，1 已经建立，2 正在关闭， 3 连接已关闭或者没有连接成功
s.send('hello')  // 发送的数据必须是纯文本
s.onopen = function(){}
s.onmessage = function(event) {
    console.log(event.data)  // 当收到消息时，数据是纯字符
}
s.close()  // 关闭连接
s.onclose = function(event) {
    // event.wasClean 是否明确的关闭
    // event.code 服务器返回的数值状态码
    // event.reason  字符串，服务器返回的消息
}
```

# WebSocket解决了什么问题
***
客户端(浏览器)和服务端进行通信，只能由客户端发起ajax请求，才能进行通信，服务端无法主动向客户端推送消息。
当出现类似体育赛事，聊天室，实时位置之类的场景时，客户端要获得服务器端的变化，就只能通过轮询(定时请求)来了解服务器端有没有新的信息变化。

`轮询效率很低，非常浪费资源(需要不断发送请求，不停链接服务器)`

WebSocket的出现，让服务器端可以主动向客户端发送信息，使得浏览器具备了实时双向通信的能力，这就是WebSocket解决的问题。

# WebSocket的class类
***
当项目中很多地方使用WebSocket，把它封装成一个class类，是更好的选择。
下面的例子，做了非常详细的注释，建个html文件也可以直接使用，websocket的常用API都放进去了。

```js
class WebSocketClass {
    /**
     * @description: 初始化实例属性，保存参数
     * @param {String} url ws的接口
     * @Param {Function} msgCallback 服务器信息的回调传数据给函数
     * @Param {String} name 可选值 用于区分ws,用于debugger
     * /
    constructor(url, msgCallback, name = 'default') {
        this.url = url;
        this.name = name;
        this.ws = null; // websockt对象
        this.status = null; // websocket是否关闭
    }

    /**
     * @description: 初始化 连接websocket或重连websocket时调用
     * @param {*} 可选值，要传的数据
     * /
    connect(data) {
        this.ws = new Websocket(this.url);
        this.ws.onopen = e => {
            this.status = 'open';
            console.log(`${this.name}连接成功`, e);
            if(data !== undefined) {
                return this.ws.send(data);
            }
        }
        // 监听服务器返回的信息
        this.ws.onmessage = e => {
            return this.msgCallback(e.data);
        }
        // ws关闭回调
        this.ws.onclose = e => {
            this.closeHandle(e); // 判断是否关闭
        }
        // ws出错回调
        this.ws.onerror = e => {
            this.closeHandle(e); // 判断是否关闭
        }
    }

    // 发送信息给服务器
    sendHandle(data) {
        return this.ws.send(data);
    }

    closeHandle(e = 'err') {
        if(this.status !== 'close') {
            this.connect();
        } else {
            console.log('关闭');
        }
    }

    closeMyself() {
        this.status = 'close';
        return this.ws.close();
    }
}

function someFn(data) {
    console.log('接受服务器消息的回调', data);
}

const wsValue = new WebSocketClass('wss://echo.websocket.org', someFn, 'wsName');
wsValue.connect('理解与服务器建立连接'); // 连接服务器
```

可以把class放在一个js文件里,export出去，然后在需要用的地方再import进来，把参数穿进去就可以了。

# WebSocket不稳定
***
WebSocket不稳定，在使用一段时间后，可能会断开连接，貌似至今没有一个为何会断开连接的公论，所以我们需要让WebSocket保持连接状态，这里推荐有两种方法。

## WebSocket设置变量，判断是否手动关闭连接
WebSocketClass类中就是用的这种方式，设置一个变量，在websocket关闭/报错的回调中，判断是不是手动关闭的，如果不是的话，就重新连接，这样做的优点如下:
* 优点: 请求较少(相对于心跳连接)，容易设置
* 缺点: 可能会导致丢失数据，在断开重连的这段时间中，恰好双方正在通信。

## WebSocket心跳机制:
> 因为第一种方案的缺点，并且可能会有其他一些未知情况导致断开连接而没有触发Error或close时间，这样就导致实际连接已经断开了，而客户端和服务端却不知道，还在傻傻的等待消息来。
然后聪明的程序员们想出了一种叫心跳机制的解决方法。
客户端就像心跳一样每隔固定的时间发送一次ping,来告诉服务器我还活着，而服务器也会返回pong，来告诉客户端，服务器还活着。

# 关于WebSocket
**
WebSocket当前的状态: WebSocket.readyState
下面是WebSocket.readyState的四个值(四种状态)
* 0: 代表正在连接
* 1: 代表连接成功，可以通信了
* 2: 代表连接正在关闭
* 3: 代表连接已经关闭或者打开连接失败
我们可以利用当前状态来做一些事情，比如上面例子中当WebSocket连接成功后，才允许客户端发送ping。

```js
if(this.ws.readyState === 1) {
    // 检查ws为链接状态 才可发送
    this.ws.send('ping'); // 客户端发送ping
}
```

## WebSocket还可以发送/接收二进制数据

## WebSocket的优点
1、双向通信
2、数据格式比较轻量，性能开销小，通信高效，协议控制的数据包头部较小，而HTTP协议每次通信都需要携带完整的头部
3、更好的二进制支持
4、没有同源限制，客户端可以与任意服务器端连接
5、与HTTP有良好的兼容性，默认端口也是80和443，并且握手阶段采用HTTP协议，因此握手时不容易屏蔽，能通过各种HTTP代理服务器。