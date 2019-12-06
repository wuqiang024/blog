# Cookie
HTTP是无状态的web通信服务器协议，什么是无状态呢？就是一次对话完成后下一次对话完全不知道上一次对话发生了什么。如果在web服务器里只是用来管理静态文件还好说，对付是谁并不重要，把文件从磁盘中读取出来发送出去即可。但是随着网络的发展，比如电商中的购物车只有记住了用户的身份才能够执行接下来的一系列动作。所以此时就需要我们无状态的服务器记住一些事情。

那么web服务器是如何记住一些事情的呢？既然web服务器记不住东西，那么我们就在外部想办法解决，相当于服务器给每个客户端都贴上了一个小纸条。上面记录了服务器给我么返回的一些信息。然后服务器看到这张小纸条就知道我们是谁了。那么Cookie是谁产生的呢？`Cookie是服务器产生的`。接下来我们描述下`Cookie`产生的过程。

* 浏览器第一次访问服务器时，服务器肯定不知道他的身份，所以创建一个特殊的身份标识数据，格式为`key=value`，放到`Set-Cookie`字段，随着响应报文发送给浏览器。

* 浏览器看到有`Set-Cookie`字段以后就知道这是服务器给的身份标识，于是就保存起来，下次请求时就会自动将`key=value`值放入到`Cookie`字段中发送到服务端。

* 服务端收到请求报文后，发现`Cookie`字段中有值，就能根据此值识别用户的身份然后提供个性化服务。

如下图所示：

![](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba0ba9f6?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

接下来我们用代码演示一下服务器是如何生成，我们自己搭建一个后台服务器，这里我们用的是SprintBoot搭建的，并且写入SprintMVC的代码如下。
```java
@RequestMapping("/testCookies")
public String cookies(HttpServletResponse response){    
	response.addCookie(new Cookie("testUser","xxxx"));
	return "cookies";
}
```
项目启动后我们输入路径`http://localhost:8005/testCookies`，然后查看发的请求。可以看到下面那张图使我们首次访问服务器发送的请求，可以看到服务器的响应中有Set-Cookie字段。而里面的`key=value`值正是我们服务器中设置的值。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba35648b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba35648b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

接下来我们再次刷新这个页面就可以看到在请求体中已经设置了Cookie字段，并且将我们的值也带过去了。这样服务器就能根据Cookie中的值记住我们的信息了。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba70165f?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba70165f?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

接下来我们换一个请求呢？是不是`Cookie`也会带过去呢？接下来我们输入路径`http://localhost:8005`请求。我们可以看到`Cookie`字段还是带过去了。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba9e5584?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ba9e5584?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

那么浏览器的`Cookie`放在哪里呢？如果是使用`Chrome`浏览器的话，可以按照以下步骤。

1、打开chrome浏览器
2、在右上角，一次点击`更多`图标 -> 设置
3、在底部点击`高级`
4、在隐私设置和安全性下方，点击网站设置
5、依次点击`Cookie` 查看所有`Cookie和网站数据`

然后可以根据域名进行搜索所管理的`Cookie`数据。所以是浏览器替你管理了`Cookie`的数据。如果此时你换成了Firefox等其他的浏览器，因为`Cookie`是存在`Chrome`里头的，所以服务器又懵圈了，不知道你是谁，就给你的`Firefox`再次贴上小纸条。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45bf5c4620?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45bf5c4620?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

## Cookie中的参数设置
说道这里，应该知道了Cookie就是服务器委托浏览器存储在客户端里的一些数据，而这些数据通常会记录用户的关键识别信息。所以`Cookie`需要一些其他的手段来保护，防止外泄或窃取，这些手段就是`Cookie`的属性。

参数名|作用|后端设置方法
-|-|-
Max-Age|设置cookie的过期时间，单位为秒|cookie.setMaxAge(10)
Domain|指定cookie所属的域名|cookie.setDomain('')
Path|指定cookie所属的路径|cookie.setPath('')
HttpOnly|告诉浏览器此cookie只能靠浏览器Http协议传输，禁止其他形式访问|cookie.setHttpOnly(true)
Secure|告诉浏览器此cookie只能在Https安全协议中传输，如果是Http则禁止传输|cookie.setHttpOnly(true)




