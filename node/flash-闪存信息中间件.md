## 需求
***

在使用express4.x开发系统的时候，需要利用session做信息的闪存服务，用于错误信息的下次页面抛出功能。
这种功能在如laravel等php框架中基本都是内置的，而express需要自己去实现。

主要做到以下两点:

* 在nodejs的业务代码中，能够flash session内容
* 在nunjucks模板中能够获取到flash的session内容，一次性获取。


## 实现
***

> 下面所有中间件均基于 `express-session`中间件已经安装的前提下

1、实现闪存session的全局中间件

> `connect-flash`是一个成熟的闪存中间件，实际项目中建议使用该中间件，下面自己实现的中间件仅阐述思想。

闪存信息的中间件原理和其他全局中间件功能其实差不多，主要就是在req上挂载一个新的方法如: flash()

而_flash()方法则是借助`express-session`的req.session属性将需要保存的数据挂载到`req.session.flash`属性上，以便其他文件获取。

> 理论上，这里的业务逻辑和安全性应当考虑更多，这里不做多考虑。

```javascript
module.exports = function flash() {
	return function(req, res, next) {
		req.flash = _flash;
		next();
	}
}

function _flash(type = false, msg = '') {
	if(msg.length == 0) {
		this.session.flash = {};
	} else {
		const status = true;
		this.session.flash = {status, type, msg};
	}
	return this.session.flash;
}
```