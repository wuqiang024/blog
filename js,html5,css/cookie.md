# cookie
***

## cookie是什么
***
cookie是当你浏览某个网站的时候，由web服务器存储在你的机器硬盘上的一个小的文本文件。他其中记录了你的用户名，密码，浏览的网页，停留的时间等信息。当你再次来到这个网站的时候，web服务器会先看看他有没有上次留下来的cookie。如果有的话，会读取cookie的内容,来判断使用者，并送出相应的网页内容。比如在网页显示欢迎你的标语或让你不用输入ID，密码就直接登录等。

当客户端要发送http请求的时候，浏览器会先检查一下是否有对应的cookie。有的话，则自动的添加在request header中的cookie字段。注意，每一次http请求时，如果有cookie，浏览器都会自动带上cookie发送给服务端。那么把什么数据放到cookie就很重要了，因为很多数据并不是每次请求都要发送给服务端，毕竟会增加网络开支，浪费带宽。所以对于那些设置`每次请求都要携带的信息`就特别适合放在cookie里，其他类型的数据就不合适了。

简单的就是说:
1、cookie是以小的文本文件形式(即纯文本)，完全存在于客户端；cookie保存了登录的凭证，有了它，只需要在下次请求时带着cookie发送，就不必再重新输入用户名、密码等重新登录了。
2、是设计用来在服务端和客户端进行信息传递的。

第一次请求时:
![https://segmentfault.com/img/remote/1460000017332171?w=606&h=274](https://segmentfault.com/img/remote/1460000017332171?w=606&h=274)

下一次请求时:
![https://segmentfault.com/img/remote/1460000017332172](https://segmentfault.com/img/remote/1460000017332172)

浏览器会把cookie放到请求头一起提交给服务器，cookie携带了会话ID信息。服务器会根据cookie辨认用户；由于cookie带了会话的ID信息，可以通过cookie找到对应对话，通过判断对话的方式来判断用户状态。

## cookie的属性
***
在浏览器中可以通过输入document.cookie来查看cookie。cookie是一个由键值对构成的字符串，每个键值对之间是'`; '`即一个分号和一个空格隔开。

`document.cookie`: 注意，这个方法只能获取非HttpOnly类型的cookie。

每一个cookie都有一定的属性，如什么时候失效，要发送到哪个域名，哪个路径等。这些属性是通过cookie选项来设置的，cookie选项包括: expires,domain,path,secure,HttpOnly。在设置任一个cookie时都可以设置相关的这些属性，当然也可以不设置，这时会使用这些属性的默认值。在设置这些属性时，属性之间由一个分号和一个空格分开。代码示例如下:
```js
"key=name; expires=Sat, 08 Sep 2018 02:26:00 GMT; domain=ppsc.sankuai.com; path=/; secure; HttpOnly"
```

cookie的属性可以在控制台查看: Application选项，左边选择Storage，最后一个就是cookie，点开即可查看。

### `* Expires, Max Age:`
Expires选项用来设置cookie什么时间内有效。Expires其实是cookie失效时间，Expires必须是GMT格式的时间(可以通过new Date().toGMTString())或者`new Date().toUTCString()`来获得。

`new Date().toGMTString()或者new Date().toUTCString()`

如expires=Sat, 08 Sep 2018 02:26:00 GMT是表示cookie将在2018年9月8日2:26分后失效。对于失效的cookie浏览器会清空。如果没有设置该选项，这样的cookie称为会话cookie。他存在内存中，当会话结束，也就是浏览器关闭时,cookie消失。

`补充:`
> Expires是http/1.0协议中的选项，在http/1.1协议中已经由Max Age代替，两者的作用都是限制cookie的有效时间。Expires的值是一个时间点(cookie失效时间=Expires),而Max Age的值是一个以秒为单位的时间段(cookie失效时间=创建时间+Max Age)。另外，Max Age的默认值是-1(即有效期为session)；Max Age有三种可能值: 负数，0，正数。
* 负数: 有效期等同于session
* 0: 删除cookie
* 正数: 有效期为创建时刻+Max Age

### `* Domain和Path`
***
Domain是域名，Path是路径，两者加起来就构成了URL，Domain和Path一起来限制cookie能被哪些URL访问。即请求的URL是Domain或其子域名，而且路径是Path或子路径，则都可以访问该cookie，例如:

某cookie的Domain为'baidu.com',Path为'/'，若请求的URL(URL可以是js/html/img/css资源请求，但是不包括XHR请求)的域名是'baidu.com'或者其子域名'api.baidu.com'，路径是'/'或子路径'/home','/home/login'，则都可以访问该cookie。

`补充:`
> 发生跨域xhr请求时，即使请求URL的域名和路径都满足cookie的Domain和Path,默认情况下cookie也不会自动被添加到请求头部中。

### `* Size`
***
cookie的大小

### `* Secure`
***
Secure选项用来设置cookie只在确保安全的请求中才会发送。当请求是HTTPS或者其他安全协议时，包含Secure选项的cookie才能被发送到服务器。

默认情况下，cookie不会带secure选项(即为空)。所以默认情况下，不管是HTTPS协议还是HTTP协议的请求，cookie都会被发送到服务端。但要注意一点，Secure选项只是限定了在安全情况下才可以传输给服务端，并不代表你能看到这个cookie。

`补充:`
如果想在客户端即网页中通过JS去设置Secure类型的cookie，必须保证网页是Https协议的。在http协议的网页中是无法设置secure类型cookie的。

### `* httpOnly`
***
这个选项用来设置cookie是否能通过js去访问。默认情况下，cookie不会带httpOnly(即为空)，所以默认情况下，客户端是可以通过js代码去访问(包括读取，修改，删除)这个cookie的。当cookie代httpOnly选项时，客户端则无法通过JS代码去访问这个cookie。

在客户端是不能通过js代码去设置一个httpOnly类型的cookie的，这种类型的cookie只能通过服务端来设置。

可以在浏览器的控制台中看出哪些cookie是httpOnly类型的。HTTP下带绿色对勾的即使。

只要是httpOnly类型的，在控制台通过document.cookie是获取不到的，也不能进行修改.

之所以限制客户端去访问cookie，主要还是出于安全目的。因为如果任何cookie都能被客户端通过document.cookie获取，那么假如合法用户的网页受到了XSS攻击，有一段恶意的脚本插入到了网页中，这个script脚本，通过document.cookie读取了用户身份验证相关的cookie，那么只要原样转发cookie，就可以达到目的了。

## cookie的设置，删除，读取方法
***
cookie既可以通过服务端来设置，也可以由客户端设置。

## 服务端设置cookie
***
客户端第一次向服务端请求时，在相应的响应头中就有set-cookie字段，用来标识是哪个用户。
下图是登录腾讯云的某个页面的响应头截图，可以看到响应头中有两个set-cookie字段，每段对应一个cookie，注意每个cookie放在一个set-cookie字段中，不能将多个cookie放在一个set-cookie字段中。具体每个cookie设置了相关的属性: expires, path, httponly
![https://segmentfault.com/img/remote/1460000017332175?w=692&h=193](https://segmentfault.com/img/remote/1460000017332175?w=692&h=193)

服务端设置cookie的范围:
服务端可以设置cookie的所有选项

## 客户端设置cookie
***
cookie不像storage有setItem,getItem,removeItem,clear等方法，需要自己封装。简单的在浏览器的控制台里输入:
`document.cookie="name=lynnshen; age=18"`
但发现只添加了第一个cookie:"name=lynnshen"，后面的cookie并没有添加进来。
最简单的设置多个cookie的方法就是重复执行document.cookie="key=name"

`注意:`
当name,domain,path这三个字段都相同的时候，cookie会被覆盖

下面是简单封装的设置，读取，删除cookie的方法:

* 设置cookie
```js
function setCookie(name, value, iDay) {
    var oDate = new Date();
    oDate.setDate(oDate.getDate() + iDay);
    document.cookie = name + '=' + value + ';expires=' + oDate;
}
```

* 读取cookie，该方法简单的认为cookie中只有一个'='，即key=value，如有更多需求可以在此基础上完善:
```js
function getCookie(name) {
    var arr = document.cookie.split('; '); // 用';'和空格来划分cookie
    for(var i = 0; i < arr.length; i++) {
        var arr2 = arr[i].split('=');
        if(arr2[0] == name) {
            return arr2[1];
        }
    }
    return ''; // 整个遍历完没找到，就返回空值。
}
```

* 删除cookie:
```js
function removeCookie(name) {
    setCookie(name, '1', -1); // 第二个value值随便设置一个，第三个值为-1表示: 昨天就过期了，赶紧删除
}
```

## cookie的缺点
***
1、每个特定域名下的cookie数量有限:
ie6或以下版本: 最多20个cookie
ie7或以上版本: 最多50个cookie
FF: 最多50个cookie
Opera: 最多30个cookie
chrome和safari没有硬性限制

2、存储量太小只有4KB；
3、每次HTTP请求都会发送到服务端，影响获取资源的效率
4、需要自己封装获取，设置，删除cookie的方法。

## cookie和session的区别
***
cookie是存在客户端浏览器上，session会话存在服务器上。会话对象用来存储特定用户会话所需的属性及配置信息。当用户请求来自应用程序的web时，如果该用户还没有会话，则服务器将自动创建一个会话对象。当会话过期或者被放弃后，服务器将会终止该会话。cookie和会话需要配合。
当cookie失效，session过期时，就需要重新登录了。

## localStorage和sessionStorage
***
在较高版本浏览器中，js提供了两种存储方式。sessionStorage和localStorage。在H5中用localStorage代替了globalStorage.

sessionStorage用于本地存储一个会话中的数据，这些数据只有在同一个会话的页面才能访问，并且当会话结束后，数据也随之销毁。所以sessionStorage仅仅是会话级别的存储，而不是一种持久化的存储。

localStorage是持久化的本地存储，除非是通过js删除，或者清除浏览器缓存，否则数据永不过时。

浏览器的支持情况: IE7及以下版本不支持web storage，其他都支持。不过在IE5,6,7中有一个userData，其实也是用于本地存储。这个持久化数据放在缓存中，只要不清理缓存，就会一直存在。

## web storage和cookie的区别
***
1、web storage和cookie的作用不同，web storage用于本地大容量存储数据(可到5M),而cookie是用于客户端和服务端间的信息传递
2、web storage有自己的方法，cookie需要我们来自己封装

