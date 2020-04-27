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