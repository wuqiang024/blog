# 核心对象

* HTTP接收解析响应
* 中间件执行上下文
* Koa中一切的流程都是中间件

# 源码组成

* application
* context
* request
* resposne

# 中间件的使用

```js
const Koa = require('koa');
cosnt app = new Koa();

const mid1 = async (ctx, next) => {
	ctx.body = 'Hi';
	await next();
	ctx.body += ' there';
};

const mid2 = async (ctx, next) => {
	ctx.type = 'text/html; chartset=utf-8';
	await next();
}

const mid3 = async (ctx, next) => {
	ctx.body += ' cheng';
	await next();
};

app.use(mid1);
app.use(mid2);
app.use(mid3);

app.listen(2333);
```