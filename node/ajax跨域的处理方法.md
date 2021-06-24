# ajax跨域的处理方法
既然跨域问题的产生原因在于浏览器的限制，那么网页端在请求时无法主动规避，此时就需要服务器端进行处理。
服务器端只需要在响应ajax需求时，在请求头中加入一个`Access-Control-Allow-Origin`属性，并设置为`*(表示全部域名)`或者是当前域名，就可以让浏览器不再进行限制。

以下示例:

```js
const http = require('http');
const server = http.createServer((req, res) {
	res.setHeader('Access-Control-Allow-Origin', '*');
	res.write(`{"resultCode:200", "msg":"success"}`);
	res.end()
})
```