# nginx技术分析
***

## nginx在应用程序中的作用
***
* 解决跨域
* 请求过滤
* 配置gzip
* 负载均衡
* 静态资源服务器

nginx是一个高性能的HTTP和反向代理服务器，也是一个通用的TCP/UDP代理服务器，最初由俄罗斯人lgor Sysoev编写。

## 正向代理和反向代理
***
代理是在服务器和客户端之前架设的一层服务器，代理接收客户端的请求并把它转发给服务器，然后将服务器的响应转发给客户端。

不管正向代理还是反向代理，实现的都是上面的功能。

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0F1ISfSTJyJwcBia2PR7NzCiaZv1DU8NHnQnT7qQHKcKBzzupaXIEnkOA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0F1ISfSTJyJwcBia2PR7NzCiaZv1DU8NHnQnT7qQHKcKBzzupaXIEnkOA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 正向代理
***
`正向代理，意思是一个位于客户端和原始服务器之间的服务器，为了从原始服务器获取内容，客户端向代理发送一个请求并指定目标(原始服务器)，然后代理向原始服务器转交请求并将获得的内容返回给客户端。`

正向代理是为我们服务的，即为客户端服务的，客户端可以根据正向代理访问到它本身无法访问的服务器资源。

正向代理对我们是透明的，对服务的是非透明的，即服务端并不知道自己收到的是来自代理的访问还是来自真实客户端的访问。

### 反向代理
***
反向代理是指以代理服务器来接收internet上的连接请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给客户端，此时代理服务器对外就表现为一个反向代理服务器。

反向代理是为服务端服务的，反向代理可以帮助服务器接收来自客户端的请求，帮助服务器做转发，负载均衡等。

反向代理对服务端是透明的，即我们并不知道自己访问的是代理服务器，而服务器知道反向代理在为他服务。

## 基本配置
***
![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0kmLc8jx1YBVXAo0o2jh0dgf7zyFRHOtiaAtJF5wAkHmTCoXEC6BwhDA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0kmLc8jx1YBVXAo0o2jh0dgf7zyFRHOtiaAtJF5wAkHmTCoXEC6BwhDA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```js
events {
    
}

http {
    server {
        location path
    }

    server {
        ...
    }
}
```

* main: nginx的全局配置，对全局生效
* events: 配置影响nginx服务器或与用户的网络连接
* http: 可以嵌套多个server，配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置
* server: 配置虚拟主机的相关参数，一个http中可以有多个server
* location: 配置请求的路由，以及各种页面的处理情况
* upstream: 配置后端服务器具体地址，负载均衡配置不可或缺的部分。

### 内置变量
***
| 变量名 | 功能 |
| -- | -- |
| $host | 请求信息中的Host，如果请求中没有Host行，则等于设置的服务器名 |
| $request_method | 客户端请求类型，如GET,POST |
| $remote_addr | 客户端的IP地址 |
| $args | 请求中的参数 |
| $content_length | 请求头中的Content-Length字段 |
| $http_user_agent | 客户端agent信息 |
| $http_cookie | 客户端cookie信息 |
| $remote_port | 客户端端口 |
| $server_protocol | 请求使用的协议，如HTTP/1.0,HTTP/1.1 |
| $server_addr | 服务器地址 |
| $server_name | 服务器名称 |
| $server_port | 服务器端口 |

### 解决跨域
***
#### 跨域的定义
***
同源策略限制了从一个源加载的文档或脚本如何与来自另一个源的资源进行交互。这是一个用于隔离潜在恶意文件的重要安全机制。通常不允许不同源之间的读操作。

### 同源的定义
***
如果两个页面的协议，端口，域名都相同，则两个页面具有相同的源。(子域名不同也属于跨域)

### nginx解决跨域的原理
***
例如:
* 前端server的域名为: fe.server.com
* 后端server的域名为: dev.server.com

现在我们在fe.server.com发起请求一定会出现跨域。

现在我们只要启动一个nginx服务器，将server_name设置为fe.server.com，然后设置相应的location以拦截前端需要跨域的请求，最后将请求代理回dev.server.com。如下配置。
```js
server {
    listen  80;
    server_name fe.server.com;
    location / {
        proxy_pass  dev.server.com;
    }
}
```
这样可以完美的绕过浏览器的同源策略:fe.server.com访问nginx的fe.server.com属于同源访问，而nginx对服务端转发的请求不会触发浏览器的同源策略。

### 请求过滤
***
根据状态码过滤
```js
error_page 500 501 502 503 504 506 /50x.html;
    location = /50x.html {
        root /root/static/html;
    }
```

根据URL名称过滤，精准匹配URL，不匹配的URL全部重定向到主页。
```js
location / {
    rewrite ^.*$ /index.html redirect;
}
```

根据请求类型过滤
```js
if($request_method !~ ^(GET|POST|HEAD)$) {
    return 403;
}
```

### 配置gzip
***
GZIP是规定的三种标准HTTP压缩格式之一。目前绝大多数网站都在使用GZIP传输。
对于文本文件，GZIP的效果非常明显，开启后传输所需流量大约会将至1/4~1/3。
并不是每个浏览器都支持gzip的，如何知道客户端是否支持gzip呢，请求头中的Accept-Encoding来标识对压缩的支持。

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0WTAJ76UdkR4bwjglBCvL7TcHKhicCASYPjHntl8ntqdWibibVIuCialesA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0WTAJ76UdkR4bwjglBCvL7TcHKhicCASYPjHntl8ntqdWibibVIuCialesA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

启用gzip同时需要客户端和服务端的支持，如果客户端支持gzip的解析，那么只要服务端能够返回gzip的文件就可以启用gzip了，我们可以通过ngxin的配置来让服务端支持gzip。下面的response中content-encoding:gzip，指服务端开启了gzip的压缩方式。

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0k7eNMibEic27Mic4CTQNfhOZLOYc3gCSxQHRpyiblCbbB4lUGtOsjd0QvA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0k7eNMibEic27Mic4CTQNfhOZLOYc3gCSxQHRpyiblCbbB4lUGtOsjd0QvA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```js
gzip    on;
gzip_http_version   1.1;
gzip_com_level  5;
gzip_min_length 1000;
gzip_types  text/csv text/html text/css text/plain text/javascript application/javascript application/x-javascript application/json application/xml;
```

`gzip`
* 开启或关闭gzip模块
* 默认值为off
* 可配置为on/off

`gzip_http_version`
* 启用gzip所需的http最低版本
* 默认为HTTP/1.1

这里为什么是HTTP/1.1而不是HTTP/1.0呢？

HTTP运行在TCP连接之上，自然也有着跟TCP一样的三次握手，慢启动等特性。

启用持久连接情况下，服务器发出响应后让TCP连接继续打开着。同一对客户/服务端之间的后续请求和响应可以通过这个连接发送。

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0tvHKvh0VgrD6tLxZpicj2CTcp4FnK4gnFMNX57ejXPeB1U6Mo8f9Ltg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0tvHKvh0VgrD6tLxZpicj2CTcp4FnK4gnFMNX57ejXPeB1U6Mo8f9Ltg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

为了尽可能的提高HTTP性能，使用持久连接就显得尤为重要了。

HTTP/1.1默认支持TCP持久连接，HTTP/1.0也可以通过显式指定Connection: keep-alive来启用持久连接。对于TCP持久连接上的HTTP报文，客户端需要一种机制来准确判断结束位置，而在HTTP/1.0中，这种机制只有Content-Length。而在HTTP/1.1中新增的Transfer-Encoding: chunked所对应的分块传输机制可以完美的解决这类问题。

nginx同样有着配置chunked的属性chunked_transfer_encoding,这个属性默认是开启的。

ngxin在启用了gzip的情况下，不会等文件gzip完成再返回响应，而是边压缩边响应，这样可以显著提高TTFB(Time To First Byte，首字节时间,web性能优化重要指标)。这样唯一的问题是,nginx开始返回响应时，它无法知道将要传输的文件最终有多大，也就是无法给出Content-Length这个响应头部。

所以，在HTTP1.O中如果利用Nginx启用了gzip，是无法获得Content-Length的，这导致HTTP1.0中开启持久链接和使用Gzip只能二选一，所以在这里gzip_http_version默认设置为1.1。

`gzip_com_level`
* 压缩级别，级别越高压缩率越大，当然压缩时间也就越长(传输快但是比较消耗CPU)
* 默认值为1
* 压缩级别取值1-9

`gzip_min_length`
* 设置允许压缩的页面最小字节，Content-Length小于该值的请求将不会被压缩。
* 默认值: 0
* 当设置的值较小，压缩后的长度可能比源文件大，建议设置1000以上。

`gzip_types`
* 要采用gzip压缩的文件类型
* 默认值: text/html(默认不压缩js/css)

## 负载均衡
***

![https://mmbiz.qpic.cn/mmbiz_jpg/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0JwTfIqe2tdkXLn4T5EHbvMTGDthHmC0ciacYoDIbzQbyKC87zOafs4Q/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_jpg/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0JwTfIqe2tdkXLn4T5EHbvMTGDthHmC0ciacYoDIbzQbyKC87zOafs4Q/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

如上面的图，众多的服务窗口，下面有很多用户需要服务，我们需要一个工具或策略来帮助我们把如此多的用户分配到每个窗口，来达到资源的充分利用以及更少的排队时间。

把前面的服务窗口想象成我们的后端服务器，而后面终端的人则是无数个客户端正在发起请求，负载均衡就是用来帮助我们将众多的客户端请求合理的分配到各个服务器，以达到服务器资源的充分利用和更少的请求时间。

`nginx如何实现负载均衡`
Upstream指定后端服务器地址列表

```js
upstream balanceServer {
    server 10.1.22.33:12345;
    server 10.1.22.34:12345;
    server 10.1.22.35:12345;
}
```

在server中拦截响应请求，并将请求转发到upstream中配置的服务器列表。

```js
server {
    server_name fe.server.com;
    listen  80;
    location /api {
        proxy_pass  http://balanceServer;
    }
}
```

上面的配置只是指定了nginx需要转发的服务端列表，并没有指定分配策略。

`nginx实现负载均衡的策略`
![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0hjsBJsakCicxialaSX1E40oiaNme2zZicohvfib0O8mEUh5B5ewicuqFzNIg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0hjsBJsakCicxialaSX1E40oiaNme2zZicohvfib0O8mEUh5B5ewicuqFzNIg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`轮询策略`
默认情况下采用的策略，将所有客户端请求轮询分配给服务器，这种策略是可以正常服务的，但是如果其中某一台服务器压力太大，出现延迟，会影响所有分配在这台服务器下的用户。

```js
upstream balanceServer {
    server 10.1.22.33:12345;
    server 10.1.22.34:12345;
    server 10.1.22.35:12345;
}
```

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0kibpD1fJoibLWGDZsj0UsF7iaywG5ReiaAewhzJDPEtdaEJ9TyppZcJxdg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0kibpD1fJoibLWGDZsj0UsF7iaywG5ReiaAewhzJDPEtdaEJ9TyppZcJxdg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`最小连接数策略`
将请求优先分配给压力较小的服务器，它可以平衡每个队列的长度，并避免向压力大的服务器添加更多请求。

```js
upstream balanceServer {
    least_conn;
    ....
}
```

![https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0CaE3syGNOGiaMsRL5SmgM7aSiamPDRzWqkJunyJAP8QVgcI00krogs3w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/XIibZ0YbvibkUOzqwBczeZM78kB0eiavfE0CaE3syGNOGiaMsRL5SmgM7aSiamPDRzWqkJunyJAP8QVgcI00krogs3w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`最快响应时间策略`
依赖于NGINX Plus,优先分配给响应时间最短的服务器。
```js
upstream balanceServer {
    fair;
}
```

`客户端IP绑定`
来自同一个IP的请求永远只分配给一台服务器，有效解决了动态网页存在的session共享问题。
```js
upstream balanceServer {
    ip_hash;
}
```

## 静态资源服务器
***
```js
location ~* \.(png|gif|jpg|jpeg)$ {
    root /root/static/;
    autoindex   on;
    access_log  off;
    expires 10h; // 设置过期时间为10小时
}
```

匹配以png|gif|jpg|jpeg为结尾的请求，并将请求转发到本地路径，root中指定的路径即nginx本地路径。同时也可以进行一些缓存的设置。