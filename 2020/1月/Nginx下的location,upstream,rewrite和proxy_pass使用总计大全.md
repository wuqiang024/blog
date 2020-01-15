# location: 顾名思义-->地址，也叫路由。
nginx服务器非常核心的配置，一般运维人员在修改nginx配置时，大部分也是围绕location进行修改。
下面看一个简单的location配置。
```js
location / {
    root    home/;
    index   index.html;
}
```
这个配置表示任何一个路径访问nginx服务器，都会跳转到home目录下的index.html页面中。

下面详细说一下location路径匹配规则，location路径匹配分为3种方式。
1、绝对匹配，完全相等“=”号，比如:

```js
// 当访问地址端口后面的等于/login/demo.html时，就会直接走location地址。
location = /login/demo.html {
    ****;
}
```

2、正则匹配~或~*。前一个区分大小写，后一个不区分大小写。

```js
location ^~ /images/ {
    // 匹配任何以/images/开头的任何查询并停止搜索。任何正则表达式将不会被测试。区分大小写。
}

location ~* .(gif|jpg|jpeg)$ {
    // 匹配任何以.gif,.jpg,.jpeg结尾的请求。不区分大小写。
}
```

3、一般匹配无符号，无符号匹配就算匹配中，也不会break，会继续向下匹配下去，如果发现或者完全匹配的情况，则直接使用。

总结一下: =严格匹配。如果这个查询匹配，那么将停止搜索并立即处理此请求。~为区分大小写匹配(可用正则表达式)。 !~为区分大小写不匹配。~*为不区分大小写匹配(可用正则表达式)。!~*为不区分大小写不匹配。^~如果把这个前缀用于一个常规字符串，那么告诉nginx如果路径匹配那么不测试正则表达式。

# proxy_pass反向代理
1、dan个我们遇到跨域问题时，而且客户端无法支持CORS时，最好的办法就是让服务器来做代理。在前端页面所在的服务器nginx配置上开一个路由，然后使用proxy去请求另一个域名下的资源。
2、前后台分离，前端独立开发后也可以通过proxy_pass来反向代理到后台服务，或者服务器部署地址不方便暴露也可以用proxy做反向代理。
简单的例子:
```js
location /login {
    proxy_pass http://www.sohu.com/;
}
```
当我们访问http://192.168.0.101:8080/login就会直接跳到搜狐首页。
需要特别注意的是: proxy后面的地址有没有斜杠。

如果我们访问的地址是http://192.168.0.1/login/index.html，如果nginx配置有斜杠，则是绝对地址，最终跳转到www.sohu.com/index.html.没有斜杠则是相对地址，最终访问www.sohu.com/login/index.html。

# rewrite重写路由，rewrite中有5种命令模式
rewrite的作用是修改uri,但是注意rewrite要有个重新匹配location的副作用。由于proxy_pass的处理阶段比location处理更晚，所以需要break掉，以防止rewrite进入下一次location匹配而丢失proxy_pass。

1、break;如下

```js
// 这个指令表示，如果/login匹配成功，则在home路径中查找demo.html文件，然后跳转到demo.html。注意这是内部跳转，浏览器上的url地址不会变，还是以/login结尾。
location /login {
    rewrite ^/  /demo.html  break;
    root    home/;
}
```

2、redirect，如下

```js
// 和break差不多，不过这个表示外部跳转，也会跳转到demo.html，浏览器地址会变成demo.html
location /login {
    rewrite ^/  /demo.html  redirect;
    root    home/;
}
```

3、permanent；和redirect类似。

4、last；如果是last修饰的话，nginx会将/demo.html地址和其他location地址进行匹配。然后找到匹配的地址，继续执行下去。这里他会执行到/demo.html的location中，然后内部跳转到demo.html页面。
```js
location /login {
    rewrite ^/  /demo.html  last;
    root    home/;
}

location /demo.html {
    rewrite ^/  /demo.html  break;
    root    home/;
}
```

5、没有修饰，就是无任何修饰符。可以看到这个rewrite后面没有任何修饰符，当没有任何修饰符的情况下，匹配中location之后，不会停止，会继续向下面的location匹配下去。直到匹配到最后一个，使用最后一个匹配到的。如下:

```js
location /login {
    rewrite ^/  /demo.html;
    root    home;
}
```

# upstream,负载配置
upstream用以配置负载的策略，nginx自带的有: 轮训/权重/ip_hash。特殊需求可以用第三方策略。

```js
upstream test {
    server 192.168.0.1:8081;
    server 192.168.0.2:8081;
}

upstream test1 {
    server 192.168.1.101:8081 weight=2;
    server 192.168.1.102:8081 weight=1;
}

upstream test2 {
    ip_hash;
    server 192.168.1.101:8081;
    server 192.168.1.102:8082;
}

server {
    listen  80;
    server_name localhost;

    location /login {
        proxy_pass  http://test/;
    }
}
```
 
当访问http://localhost/login时，nginx就会在server 192.168.0.101:8081和server 192.168.0.2:8081这两个服务之间轮流访问。

upstream test1 表示上面的服务访问2次，下面的服务访问1次
upstream test2 表示根据客户端ip地址的hash值来进行区分访问那个服务，这种设置后，同一个客户端访问的服务一般是不会变的。