# 简介
***
curl是常用的命令行工具，用来请求web服务器。他的名字就是客户端(client)的URL工具的意思.
他的功能非常强大,命令行参数多达几十种.如果熟练的话,完全可以取代Postman这一类的图形界面工具。

不带有任何参数的时候，curl就是发出Get请求。

```js
curl https://www.example.com
```
上面命令向`www.example.com`发出GET请求，服务器返回的内容将会在命令行输出。

## -A
***
`-A`参数指定客户端的用户代理标头，即`User-Agent`。curl的默认用户代理字符串是`curl/[version]`。

```js
curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
```

上面命令将`User-Agent`改成chrome浏览器。

```js
curl -A '' https://google.com
```

上面命令会移除`User-Agent`标头。
也可以通过`-H`参数指定标头，更改`User-Agent`。

```js
curl -H 'User-Agent: php/1.0' https://google.com
```

## -b
***
`-b`参数用来向服务器发送Cookie。

```js
curl -b 'foo=bar' https://google.com
```

上面的命令会生成一个标头`Cookie: foo=bar`，向服务器发送一个名为foo,值为bar的Cookie。

```js
curl -b 'foo=bar;foo2=bar2' https://google.com
```

上面命令发送两个Cookie。

```js
curl -b cookies.txt https://google.com
```

上面命令读取本地文件`cookie.txt`，里面是服务器设置的Cookie(参见-c参数)，将其发送到服务器。

## -c
***
`-c`参数将服务器设置的cookie写入一个文件

```js
curl -c cookies.txt https://www.google.com
```

## -d
`-d`参数用于发送POST请求的数据体。

```js
curl -d 'login=emma&password=123` -X POST https://google.com
// 或者
curl -d 'login=emma' -d 'password=123' -X POST https://google.com
```

使用`-d`参数以后，HTTP请求会自动加上标头`Content-Type: application/x-www-form-urlencoded`。并且会自动将请求转为POST，因此可以省略`-X POST`.

`-d`参数可以读取本地文本文件的数据，向服务器发送。

```js
curl -d '@data.txt` https://google.com
```
上面命令读取`data.txt`文件的内容，作为数据体向服务器发送。

## --data-urlencode
***
`--data-urlencode`参数等同于`-d`，发送POST请求的数据体，区别在于会自动将发送的数据进行URL编码。

```js
curl --data-urlencode 'comment=hello world' https://google.com
```
上面代码中，发送的数据`hello world`之间有一个空格，需要进行URL编码。

## -e
***
`-e`参数用来设置HTTP的标头`Referer`，表示请求的来源。

```js
curl -e 'https://google.com?q=example` https://google.com
```

上面命令将`Referer`标头设为`https://google.com?q=example`
`-H`参数可以通过直接添加标头`Referer`达到同样效果。

```js
curl -H 'Referer: https://google.com?q=example' https://google.com
```

## -F
***
`-F`参数用来向服务器上传二进制文件。

```js
curl -F 'file=@photo.png' https://google.com
```
上面命令会给HTTP请求加上标头`Content-Type: multipart/form-data`，然后将文件`photo.png`作为file字段上传。
`-F`参数可以指定MIME类型。

```js
curl -F 'file=@photo.png;type=image/png' https://google.com
```

上面命令指定MIME类型为`image/png`，否则curl会把MIME类型设为`application/octet-stream`。
`-F`参数也可以指定文件名。

```js
curl -F 'file=@photo.png;filename=me.png;type=image/png' https://google.com
```
上面命令中，原始文件名为photo.png,但是服务器收到的文件名为me.png。

## -G
***
`-G`参数用来构造URL的查询字符串。

```js
curl -G -d 'q=kitties' -d 'count=20' https://google.com/search
```

上面命令发出一个GET请求，实际请求的URL为`https://google.com/search?q=kitties&count=20`，如果省略`-G`，会发出一个POST请求。
如果数据需要URL编码，可以结合`--data-urlencode`参数。

```js
curl -G --data-urlencode 'comment=hello world' https://google.com
```

## -H
***
`-H`参数添加HTTP请求的标头。
```js
curl -H 'Accept-Language: en-US' https://google.com
```
上面命令添加HTTP标头`Accept-Language: en-US`。

```js
curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://google.com
```
上面命令添加两个标头。

```js
curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' https://google.com
```
上面命令添加HTTP请求标头`Content-Type: application/json`，然后用`-d`参数发送json数据。

## -i
***
`-i`参数打印出服务器回应的HTTP标头。
```js
curl -i https://google.com
```
上面命令收到服务器回应后，先输出服务器回应的标头，然后空一行，再输出网页源码。

## -I
***
`-I`参数向服务器发出HEAD请求，然后将服务器返回的HTTP打印出来。
```js
curl -I https://google.com
```
上面命令输出服务器对HEAD请求的回应。
`--head`参数等于`-I`

```js
curl --head https://google.com
```

## -k
***
`-k`参数指定跳过SSL检测
```js
curl -k https://google.com
```
上面命令不会检查服务器的SSL证书是否正确。

## -L
***
`-L`参数会让HTTP请求跟随服务器的重定向，curl默认不跟随重定向。
```js
curl -L -d 'tweet=hi' https://api.tweetter.com/tweet
```

## --limit-rate
***
`--limit-rate`用来限制HTTP请求和回应的带宽，模拟慢网速的环境。
```js
curl --limit-rate 200k https://google.com
```
上面命令将带宽限制在每秒200K字节。

## -o
***
`-o`参数将服务器的回应保存成文件，等同于`wget`命令。
```js
curl -o example.html https://google.com
```
上面命令将`www.google.com`保存成`example.html`。

## -O
***
`-O`参数将服务器回应保存成功文件，并将URL的最后部分当做文件名。
```js
curl -O https://example.com/foo/bar.html
```
上面命令将服务器回应保存为文件，文件名为bar.html。

## -s
***
`-s`参数将不输出错误和进度信息。
```js
curl -s https://google.com
```
上面命令一旦发生错误，不会显示错误信息，不发生错误的话，会正常显示执行结果。
如果想让curl不产生任何输出，可以使用以下命令。

```js
curl -s -o /dev/null https://google.com
```

## -S
***
`-S`参数指定只输出错误信息，通常与`-s`一起使用。
```js
curl -s -o /dev/null https://google.com
```
上面命令没有任何输出，除非发生错误。

## -u
***
`-u`参数用来设置服务器认证的用户名和密码
```js
curl -u 'bob:1233' https://google.com
```
上面命令设置用户名为bob,密码为1233，然后将其转为HTTP标头`Authorization: Basic uy...`。
curl能够识别URL里面的用户名和密码。

```js
curl https://bob:1233@google.com/login
```
上面命令能够识别URL里的用户名密码，并将其转为上个例子里的HTTP标头。

```js
curl -u 'bob' https://google.com/login
```
上面命令只设置了用户名，执行后，curl会提示用户输入密码。

## -v
***
`-v`参数输出通信的整个过程，用于调试
```js
curl -v https://example.com
```
`--trace`参数也可以用于调试，还会输出原始的二进制数据。
```js
curl --trace https://google.com
```

## -x
***
`-x`参数指定HTTP请求的代理。
```js
curl -x socks5://james:cats@myproxy.com:8080 https://example.com
```
上面命令指定HTTP请求通过`myproxy.com:8080`的socks5代理发出。
如果没有指定代理协议，默认为HTTP.
```js
curl -x james:cats@myproxy.com:8080 https://example.com
```
上面命令中，请求的代理使用HTTP协议。

## -X
***
`-X`参数指定HTTP请求的方法。
```js
curl -X POST https://google.com
```
上面命令对`https://google.com`发出POST请求。