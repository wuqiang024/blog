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

下面简单演示下这几个参数的用法及现象。

## Path
设置为cookie.setPath('/testCookies')，接下来我们访问 `http://localhost:8005/testCookies`，我们可以看到在左边和我们指定的路径是一样的，所以Cookie才在请求头中出现，接下来我们访问`http://localhost:8005`，我们发现没有	`Cookie`字段了，这就是Path控制路径

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45bf715e27?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45bf715e27?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

## Domain
设置为`cookie.setDomain('localhost')`，接下来我们访问`http://localhost`我们发现下图中左边的是有`Cookie`字段的，但是我们访问`http://172.16.42.81`，看下图右边可以看到没有`Cookie`的字段了，这就是`Domain`控制的域名发送`Cookie`。
![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45da6ff7ce?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45da6ff7ce?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

# Session

> Cookie是存储在客户端，Session是存储在服务器端，客户端只存储SessionId

在上面我们了解了什么是Cookie，既然浏览器已经通过`Cookie`实现了有状态的请求，那为什么又来了个Session呢？我们想象一下，如果将账户的一些信息都存入了Cookie中的话，一旦信息被拦截，那么我们所有的账号信息都会丢失掉。所以就出现了Session，在一次会话中将重要的信息保存在Session中，浏览器只记录SessionId。一个SessionId对应一次会话请求。
![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45da01643c?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45da01643c?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

服务器在返回头中在Cookie中生成了一个SessionId。然后浏览器记住此SessionId下次访问时可以带着此Id,然后就能根据此Id找到存储在服务端的信息了。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45e2866b2d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45e2866b2d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

此时我们访问路径`http://localhost:8005/testGetSession`，发现得到了我们上面存储在Session中的信息。那么Session什么时候过期额？

* 客户端: 和Cookie过期一致，如果没设置，默认是关了浏览器就没了，即再打开浏览器的时候初次请求头中是没有SessionId了。
* 服务端: 服务端的过期是真的过期，即服务端的Session存储的数据结构多久不可用了。默认是30分钟

既然我们知道了Session是在服务端进行管理的，那么或许你们看到这有几个疑问，Session是在哪创建的？Session是存储在什么结构中？接下来带大家一起看一下Session是如何被管理的。

Session的管理是在容器中被管理的，什么是容器呢？Tomcat，Jetty等都是容器。

> Session是存储在Tomcat的容器中，所以如果后端机器是多台的话，因此多个机器间是无法共享Session的，此时可以使用Spring提供的分布式Session的解决方案，是将Session放在了Redis中。

# Token
Session是将要验证的信息存储在服务端，并以SessionId核数据进行对应，SessionId由客户端存储，在请求时将SessionId也带过去，因此实现了状态的对应。而Token是在服务器端将用户信息经过Base64Url编码过后传给客户端，每次用户请求的时候都会带上这一段信息，因此服务端拿到此信息进行解密后就知道此用户是谁了，这个方法叫JWT(Json Web Token)。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ec932e38?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45ec932e38?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

`Token相比较于Session的优点在于，当后端系统有多台时，由于是客户端访问时直接带着数据，因此无需做共享数据的操作。`

## Token的优点
1、简洁: 可以通过URL,POST参数或者是在HTTP头参数发送，因为数据量最小，传输速度也快。
2、自包含: 由于串包含了用户所需要的信息，避免了多次查询数据库
3、因为Token是以Json的形式保存在客户端，所以JWT是跨语言的
4、不需要在服务器端保存会话信息。特别适用于分布式服务。

## JWT的结构
实际的JWT大概长下面这样，他是一个很长的字符串，中间用`.`分割成三部分。
![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45f8068493?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a45f8068493?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

JWT是有三部分组成的

### Header
是一个Json对象，描述JWT的元数据，通常是下面这个样子。
```js
{
	"alg": "HS256",
	"typ": "JWT"
}
```
上面代码中，alg代表签名算法(algorithm),默认是HMAC SHA256(写成HS256);typ属性表示这个令牌(token)的类型(type)，JWT令牌统一写为JWT。

最后，将上面的JSON对象使用Base64URL算法转成字符串。

>JWT作为一个令牌，有些场合可能放到URL。Base64有三个字符+、/和=，在URL里有特殊含义，所以要被替换掉：=被省略、+被替换成-、/被替换成_。这就是Base64URL算法。

### Payload
Payload部分也是一个Json对象，用来存放实际需要传输的数据，JWT官方规定了下面几个官方的字段供选用。
* iss(issue): 签发人
* exp(expiration time): 过期时间
* aud(audience): 观众
* nbf(Not Before): 生效时间
* iat(Issued At): 签发时间
* jti(JWT ID): 编号
当然除了官方提供的这几个字段，我们也能够自己定义私有字段，下面就是一个例子。
```js
{
	"name": "xiaoming",
	"age": 14
}
```
默认情况下JWT是不加密的，任何人只要在网上进行Base64的解码就可以读到信息，所以一般不要将秘密放在这个部分。这个JSON对象也要用Base64URL算法转成字符串。

### Signature
Signature部分是对前面两个部分进行签名，防止数篡改。
首先需要定义一个密钥，这个密钥只有服务器才知道，不能泄露给用户，然后使用Header中指定的签名算法(默认是HMAC SHA256),算出签名后将Header、Payload、Signature三部分拼成一个字符串，每个部分用`.`分隔开，就可以返回用户了。

> HS256可以使用单个密钥为给定的数据样本创建签名，当消息与签名一起传输时，接收方可以使用相同的密钥来验证签名是否与消息匹配。

![https://user-gold-cdn.xitu.io/2019/12/2/16ec5a4603cefcdd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/2/16ec5a4603cefcdd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

# 总结
* Cookie是存储在客户端的
* Session是存储在服务器端的，可以理解为一个状态列表。拥有一个唯一会话标志SessionId。可以根据SessionId在服务端查询到存储的信息。
* Session会引发一个问题，即后端多台机器时Session共享的问题，解决方案可以使用Spring提供的框架。
* Token类似一个令牌，无状态的，服务端所需的信息被Base64编码后放到Token中，服务器可以直接解码出其中的数据。