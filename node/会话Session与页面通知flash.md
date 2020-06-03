## 会话
***
由于HTTP协议是无状态的协议，所以服务器需要记录用户的状态时，就需要用某种机制来识别具体的用户，这个机制就是会话(Session)。

## Cookie与Session的区别
***
1、cookie存储在浏览器，有大小限制，session存储在服务器，无大小限制
2、通常session是基于cookie的，session id存储于cookie中
3、session更安全，cookie可以直接在浏览器查看编辑

我们通过引入express-session中间件实现对会话的支持。
```javascript
app.use(session(options));
```

session中间件会在req上添加session对象，即req.session初始值为{}，当我们登陆后设置req.session.user = 用户信息，返回浏览器的头信息中会带上`set-cookie`将session id写到cookie中，那么当用户下次请求时，通过带上来的cookie中的session id我们就可以查到该用户，并将用户信息保存到req.session.user。

## 页面通知
***
我们还需要这样一个功能，当我们操作成功时需要显示一个成功的通知，如登录成功跳转到主页，需要显示一个登录成功的通知，当我们操作失败时需要显示一个失败的通知等。通知只显示一次，刷新后小时，我们可以通过connect-flash这个中间件实现。

connect-flash是基于session实现的，他的原理很简单: 设置初始值req.session.flash = {}, 通过req.flash(name, value)设置这个对象下的字段和值，通过req.flash(name)获取这个对象下的值，同时删除这个字段。实现了只显示一次后刷新后消失的功能。

## express-session, connect-mongo, connect-flash的区别和联系
***
1、express-session是会话支持中间件
2、connect-mongo将session存储于mongodb,需结合express-session使用，我们也可以将session存储于redis，如connect-redis
3、connect-flash 基于session实现的用于通知功能的中间件，需结合express-session使用。