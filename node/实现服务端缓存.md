# 关于中间件

谈到中间件，Express官网对他的阐述是这样的。

> Express是一个自身功能极简，完全是路由和中间件构成的一个web开发框架：从本质上来说，一个Express应用就是在调用各种中间件。

也许你使用过各种各样的中间件进行开发，但是并不理解中间件原理，也没用深入过Express源码，探究其实现。这里并不打算长篇大论帮您分析，但是使用层面上大致可以参考下图。

![https://user-gold-cdn.xitu.io/2017/9/6/ce32aa50d443f9edbecee7184678d355?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2017/9/6/ce32aa50d443f9edbecee7184678d355?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

# 关于服务端缓存

缓存已经被广泛使用，来提高页面性能。一说到缓存，可能读者脑海里马上冒出来：'客户端缓存，CDN缓存，服务器端缓存...'。另一维度上，也会想到: "200(from cache), expire, eTag..."等概念。

当然作为一个前端开发者，我们一定要明白这些缓存概念，这些缓存理念是相对于某个具体用户访问来说的，性能优化体现在单个用户上。比如说，我第一次打开页面A，耗时较长，下次打开页面由于缓存的作用，时间缩短了。

但是在服务器端，还存在另一个维度，思考下这样的场景:

我们有一个静态页面B，这个页面服务端需要从数据库获取部分数据b1，根据b1又要计算得到部分数据b2，还得做各种高复杂度操作，最终才能东拼西凑出需要返回的完整页面B，整个过程耗时2S。

那么面临的困境是，user1打开页面时耗时2S，user2打开同样耗时2S，而这些页面都是静态页面B，内容完全一样。为了解决这个灾难，这时候我们需要缓存，这种缓存就叫做服务端缓存(server-side cache)。

总结一下，服务端缓存的目的其实就是对于一个页面请求，而返回(缓存的)同样的页面内容。这个过程完全独立于不同的用户。

因此，下面展示的demo在第一次请求到达时，服务端耗时5秒来返回HTML;而接下来再次请求该页面，会命中缓存，不管是哪个用户访问，只需要几毫秒就可得到完整页面。

# demo

```js
'use strict'

const mcache = require('memory-cache');

const cache = (duration) => {
	return (req, res, next) => {
		let key = '__express__' + req.originUrl || req.url;
		let cacheBody = mcache.get(key);
		if(cacheBody) {
			res.send(cacheBody);
			return;
		} else {
			res.sendResponse = res.send;
			res.send = (body) => {
				mcache.put(key, body, duration * 1000);
				res.sendResponse(body);
			}
			next()
		}
	}
}
```

为了简单，我们使用了请求URL作为cache的key:
* 当它(cache key)及对应的value值存在时，便直接返回value值；
* 当它(cache key)及对应的value值不存在时，我们将对Express send方法做一层拦截：在最终返回前，存入这对key-value。

缓存的有效时间是10秒。

最终在判断之外，我们的中间件把控制权交给下一个中间件。

最终使用和测试如下代码:

```js
app.get('/', cache(10), (req, res) => {
	setTimeout(() => {
		res.render('index', {})
	}, 5000)
})
```

## 几个小问题
仔细看一下我们的页面，再去体会下实现代码，会发现一个问题，刚才我们缓存了整个页面，并将date: new Date()传入jade模板里。那么在命中缓存的条件下，10秒内，页面无法动态刷新来同步，直到10秒缓存到期。

同时，我们什么时候可以使用上述中间件，进行服务端缓存呢？当然是静态内容才可以使用。同时，PUT,DELETE,POST等操作都不该进行类似的缓存处理。

同样，我们使用了memory-cache模块，他存在的优缺点如下:
* 读写迅速简单，不需要其他依赖
* 当服务器或者这个进程挂掉的时候，缓存中的内容会全部丢失
* memcache是将缓存内容放在了自己进程的内存中，所以这个部分无法在多个Node进程之间共享

如果这些弊端很重要，在实际开发中我们可以选择分布式cache服务，比如Redis。同样你可以在npm上找到express-redis-cache模块。