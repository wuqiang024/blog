Express响应HTTP请求的response对象中有两个用于URL跳转方法`res.location()`和`res.redirect()`，使用他们可以实现URL的301或302重定向。

## res.location(path)
```
res.location('/foo/bar');
res.location('http://www.sohu.com');
res.location('back');
```
路径back具有特殊的意义，这个涉及到请求头Referer中指定的URL，如果Referer头没有指定，将会设置为`'/'`。
Express通过Location头将指定的URL字符串传递给浏览器，他并不会对指定的字符串进行验证`(除back外)`。而浏览器则负责将当前URL重定义到响应头Location中指定的URL。

## res.redirect([status], path)
其中参数:
* status: { Number } 表示要设置的HTTP状态码
* path: { String }, 要设置到Location头中的URL
使用指定的HTTP状态码，重定向到指定的URL，如果不指定HTTP状态码，使用默认的状态码"302": "Found"。而浏览器则负责将当前URL重定义到响应头Location中指定的URL。
```javascript
res.redirect('/foo/bar');
res.redirect('http://www.sohu.com');
res.redirect(301, 'http://www.sohu.com');
res.redirect('../login');
```
重定向可以是一个完整的URL，这样会重定向到一个不同的站点上。
```javascript
res.redirect('http://google.com');
```
重定向也可以相对于所在主机的根目录
```javascript
res.redirect('/admin');
```
重定向也可以相对于当前的URL，例如: 从http://www.sohu.com/blog/admin/这个地址(注意反斜杠)，下面的代码将会重定向到地址http://www.sohu.com/blog/admin/post/new
```javascript
res.redirect('post/new')
```
在从地址: http://www.sohu.com/blog/admin重定向到post/new，如果没有反斜杠的话将会重定向到http://www.sohu.com/blog/post/new

相对路径的重定向也是允许的，如果你的地址是http://www.sohu.com/admin/post/new，下面的代码将会重定向到http://www.sohu.com/admin/post这个地址:
```javascript
res.redirect('..');
```

back重定向，重定向到请求的Referer，当没有Referer请求头的情况下，默认为`'/'`。而浏览器则负责将当前URL重定义到响应头Location中指定的URL。

进行URL重定向时，服务器只在响应信息的HTTP头信息中设置了HTTP状态码和Location头信息。
当状态码为301或302时(301表示永久重定向，302表示临时重定向)，表示资源位置发生了改变，需要进行重定向。
Location头信息表示了资源的改变位置，即：要重定向的URL。

## location()与redirect()的比较
Express的response对象，是对Node原生对象ServerResponse的扩展。location()方法只会设置Location头，而redirect()方法除了会设置Location头还可以自动或手动设置HTTP状态码，理论上两者都可以实现重定向。

location()方法的实现过程如下:
```javascript
res.location = function(url) {
	var req = this.req;
	if('back' == url) url = req.get('Referer') || '/';

	this.setHeader('Location', url);
	return this;
};
```
从以上代码可以看出，location()方法本质上是调用了ServerResponse对象的setHeader()方法，但是没有设置状态码。通过location()设置头信息后，其后的代码还会执行。
使用location()方法实现重定向，还要手动设置HTTP状态码。
```javascript
res.location('http://sohu.com');
res.statusCode = 301;
```
如果需要立即返回响应信息，还要调用end()方法。
```javascript
res.location('http://www.sohu.com');
res.statusCode = 301;
res.end('响应的内容');
或
res.location('http://www.sohu.com');
res.sent(302);
```

redirect()的实现方法如下:
```javascript
res.redirect = function(url) {
	var head = 'HEAD' == this.req.method;
	var status = 302;
	var body;
	...
	this.location(url);
	...
	this.statusCode = status;
	this.set('Contennt-Length', Buffer.byteLength(body));
	this.end(head ? null : body);
}
```

从以上可以看出，redirect()方法是对location()方法的扩展。通过location()设置Location头后，设置HTTP状态码，最后通过ServerResponse对象的end方法返回响应信息。调用redirect()方法后，其后的代码都不会执行。

## 重定下与不重定向
在使用过程中，redirect()方法大多数能重定向成功，而location()则不太确定。这与我们的用法有关。
上面讲过，URL重定向是浏览器端完成的，而URL重定向与HTTP状态码和Location头有关。浏览器首先会判断状态码，只要当状态码为301和302时，才会根据Location头中的URL进行跳转。
所以使用location()设置头信息，而不设置状态码或者状态码不是301或302时，并不会发生重定向
```javascript
res.location('http://www.sohu.com');
res.sent(200);
```
而使用redirect()设置的状态码不是301或302也不会发生跳转。
```javascript
res.redirect(200, 'http://www.sohu.com');