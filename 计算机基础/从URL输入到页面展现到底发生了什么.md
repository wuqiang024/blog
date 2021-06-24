# 从URL输入到页面展现到底发生了什么
***

![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPes8jYjqZ8cXyJHTBmia94ic7uCFWPEEacPAdibIY6EwAxwh92opa7q8Vg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPes8jYjqZ8cXyJHTBmia94ic7uCFWPEEacPAdibIY6EwAxwh92opa7q8Vg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

总体来说分为以下几个过程:

* DNS解析: 将域名解析成DNS地址
* TCP连接: TCP三次握手
* 发送HTTP请求
* 服务器处理请求并返回HTTP报文
* 浏览器解析渲染页面
* 断开连接: TCP四次挥手

## URL到底是啥
***
URL(Uniform Resource Location)，统一资源定位符，用于定位网上资源，俗称网址。
比如`http://www.w3scholl.com.cn/html/index.asp`,遵守以下语法规则:

`scheme://host.domain:port/path/filename`
各部分解释如下:

* scheme: 定义因特网服务的类型，常见的协议有http, https, ftp, file，其中最常见的类型是http，而https是进行加密的网络传输。
* host: 定义域主机(http的默认主机是www)
* domain: 定义英特网域名，比如w3cschool.com.cn
* port: 定义主机上的端口(http的默认端口是80)
* path: 定义服务器上的路径
* filename: 定义文档/资源的名称

## 域名解析
***
在浏览器输入网址后，首先要经过域名解析，因为浏览器并不能直接通过域名找到相应的服务器，而是要通过IP地址。

1、IP地址
IP地址是指互联网协议地址，是IP Address的缩写，IP地址是IP协议提供的一种统一的地址格式，他为互联网上的每一个网格和每一台主机分配一个逻辑地址，以此来屏蔽物理地址的差异。IP地址是一个32位的二进制，比如127.0.0.1位本机IP。
域名就相当于IP地址乔装打扮的伪装者，带着一副面具。他的作用就是便于记忆和沟通的一组服务器的地址。用户通常使用主机名或域名来访问对方计算机，而不是直接通过IP地址访问。因为与IP地址的一组纯数字相比，用字母配合数字的表现形式来指定计算机更符合人类的记忆习惯。但是要让计算机去理解名称，相对而言就变得困难了。因为计算机更擅长处理一长串数字。为了解决上述问题，DNS服务应运而生。

2、什么是域名解析
***
DNS协议提供通过域名查找IP地址，或逆向从IP地址反查域名的服务。DNS是一个网络服务器，我们的域名解析简单来说就是在DNS上记录一条信息记录。
例如`baidu.com 220.114.23.45(外网服务器地址) 80 (服务器端口号)`

3、浏览器如何通过域名去查询URL对应的IP呢
* 浏览器缓存: 浏览器会按照一定的频率缓存DNS记录
* 操作系统缓存: 如果浏览器缓存中找不到需要的DNS记录，就去操作系统找
* 路由缓存: 路由器也有DNS缓存
* ISP的DNS服务器: IS是互联网服务提供商(Internet Service Provider)的简称，ISP有专门的DNS服务器对应DNS查询请求
* 根服务器: ISP的DNS服务器还查不到的话，他就会向根服务器发出请求，进行递归查询(DNS服务器先问根服务器.com域名服务器的IP地址，然后再问.baidu域名服务器，依次类推)

4、小结
***
浏览器通过DNS服务器发送域名，DNS服务器查询到与域名对应的IP地址，然后返回给浏览器，浏览器再将IP地址打在协议上，同时请求参数也会在协议搭载，然后一并发送给对应的服务器。接下来介绍向服务器发送HTTP请求阶段，HTTP请求分为三个阶段：TCP三次握手，http请求响应信息，关闭TCP连接。

![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPTNOkoQjHBcib9avUWRvIZ6DdkqJloUicaUOeRnULWicQtoz1aqAINicHdw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPTNOkoQjHBcib9avUWRvIZ6DdkqJloUicaUOeRnULWicQtoz1aqAINicHdw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## TCP三次握手
***
在客户端发送数据之前会发起TCP三次握手用以同步客户端和服务端的序列号和确认号，并交换TCP窗口大小信息。
![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPhCOzfMfwO9nLxHs29VatptRQxZTXv9BBhYt1wibUic0BQ7Bg3lqFG96w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPhCOzfMfwO9nLxHs29VatptRQxZTXv9BBhYt1wibUic0BQ7Bg3lqFG96w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

1、TCP三次握手的过程如下:
* 客户端发送一个带SYN=1, Seq=X的数据包到服务器端口(第一次握手，由浏览器发起，告诉服务器我要发送请求了)
* 服务器发回一个带SYN=1, ACK=X+1, Seq=Y的响应包以示传达确认信息(第二次握手，由服务器发起，告诉浏览器我准备好接受了，你赶紧发吧)
* 客户端再传回一个带ACK=Y+1,Seq=Z的数据包，代表握手结束(第三次握手，由浏览器发起，告诉服务器，我马上就发了，准备接受吧)

2、为啥需要三次握手
***
防止已失效的连接请求报文段突然又传送到服务端，因而产生错误。

## 发送HTTP请求
***
TCP三次握手结束后，开始发送HTTP请求报文
请求报文由请求行，请求头，请求体三个部分组成。

1、请求行包括请求方法，URL，协议版本
* 请求方法包括8种: GET,POST,PUT,DELETE,OPTIONS,HEAD,PATCH,TRACE
* URL即请求地址，由<协议>://<主机名>:<端口>/<路径>?<参数>组成
* 协议版本即HTTP版本号
`POST /chapter17/user.html HTTP/1.1`

以上代码中POST代表请求方法，'/chapter17/user.html'代表URL，'HTTP/1.1'代表协议和协议的版本，现在比较流行的是HTTP/1.1版本。

2、请求头包含请求的附加信息，由关键字/值对组成，每行一对，关键字和值用英文冒号':'分隔。
请求头部通知服务器有关客户端请求的信息。它包含许多有关的客户端环境和请求正文的有用信息。比如: Host，表示主机名，虚拟主机；Connection, HTTP/1.1增加的，使用keep-alive，即持久连接，一个连接可以发多个请求；User-Agent，请求发出者，兼容性以及定制化需求。

3、请求体，可以承载多个请求参数的数据，包含回车符，换行符和请求数据，并不是所有的请求都具有请求数据。
`name=tom&password=1234&realName=tomson`
上面代码，承载着name,password,realName三个请求数据。

## 服务器处理请求并返回HTTP报文
***
1、服务器
服务器是网络环境中的高性能计算机，他侦听网络上的其他计算机(客户机)提交的服务请求，并提供相应的服务，比如网页服务，文件下载服务，邮件服务，视频服务。而客户端的主要功能是浏览网页，看视频，听音乐，两者截然不同。每台服务器上都会安装处理请求的应用-web server。常见的web server产品有apache,nginx,iis或Lighttpd等。
web server担任管控的角色，对于不同用户发出的请求，会结合配置文件，把不同请求委托给服务器上处理相应请求的程序进行处理，然后返回后台程序处理的结果作为响应。

2、MVC后代处理阶段
后台开发现在有很多框架，但大部分还是按照MVC设计模式进行搭建的。
MVC是一个设计模式，将应用分为三个核心部件：模型(Model)--试图(View)--控制器(Controler)，他们各自处理自己的任务，实现输入，处理和输出的分离。

![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPumFHCcBJQ7TnqCbTwh9UOcjI7micUk8IVZCyGXJgH9EiaJWnJ96E9fyg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPumFHCcBJQ7TnqCbTwh9UOcjI7micUk8IVZCyGXJgH9EiaJWnJ96E9fyg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

* 视图(View): 他是提供给用户的操作界面，是程序的外壳
* 模型(Model): 模型主要承担数据交互，在MVC的三个部件中，模型拥有最多的处理任务。一个模型能为多个视图提供数据
* 控制器(Controller): 他负责根据用户从视图输入的指令，选取模型中的数据，然后对其进行相应的操作，产生最终的结果。控制器属于管理者角色，从视图接受请求并决定调用哪个模型构建去处理请求，然后再决定用哪个视图来显示模型处理返回的数据。

简而言之，首先浏览器发过来的请求先通过控制器，控制器进行逻辑处理后将渲染好的页面，响应信息会以响应报文的形式返回给客户端，最后浏览器通过渲染引擎将网页展现在用户面前。

## http响应文
***
响应报文由响应行，响应头，响应主体三个部分组成。

1、响应行包括: 协议版本，状态码，状态码描述

状态码规则如下:
1xx: 指示信息--表示请求已接收，继续处理
2xx: 成功--表示请求已经被成功接收，理解，接收
3xx: 重定向--表示完成请求要有更进一步的操作
4xx: 客户端错误--请求有语法错误或请求无法实现
5xx: 服务端错误--服务端未能实现合法的请求

2、响应头部包含响应报文的附加信息，由名/值对组

3、响应主体包括回车符，换行符，和响应返回数据，并不是所有响应都有响应数据

## 浏览器解析渲染页面
***
浏览器拿到响应文本HTML后，接下来介绍下浏览器渲染机制

![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXP4ArBAkEzzuF4GJvicXhHRUQ6GcrQud1ZyMtX9fb7WQnK07nughdECoA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXP4ArBAkEzzuF4GJvicXhHRUQ6GcrQud1ZyMtX9fb7WQnK07nughdECoA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

浏览器解析渲染页面分为以下五个步骤:

* 根据HTML解析出DOM树
* 根据CSS解析生成CSS规则树
* 结合DOM树和CSS规则树，生成渲染树
* 根据渲染树计算每一个节点的信息
* 根据计算好的信息绘制页面

1、根据HTML解析DOM树
* 根据HTML的内容,将标签按照结构解析称为DOM树，DOM树解析的过程是一个深度优先遍历，即先构建当前节点的所有子节点，再构建下一个节点
* 在读取HTML文档，构建DOM树的过程中，若遇到Script标签，则DOM树的构建会暂停，直至脚本执行完毕。

2、根据CSS解析生成CSS规则树
* 解析CSS规则树时JS执行将暂停，直到CSS规则树就绪
* 浏览器在CSS规则树生成之前不会进行渲染

3、结合DOM树和CSS规则树，生成渲染树
* DOM树和CSS规则树都准备好以后，浏览器才开始构建渲染树
* 精简CSS可以加快CSS规则树的构建，从而加速页面响应速度

4、根据渲染树计算每一个节点的信息(布局)
* 布局: 通过渲染树中渲染对象的信息，计算出每一个渲染对象的位置和尺寸
* 回流: 在布局完成后，发现某个部分发生了变化影响了布局，那就需要倒回去重新渲染。

5、根据计算好的信息绘制页面
* 绘制阶段，系统会遍历呈现树，并调用呈现树的paint方法，将呈现树的内容显示在屏幕上
* 重绘: 某个元素的背景颜色，文字颜色，不影响元素周围或内部布局的属性，将只会引起浏览器的重绘
* 回流: 某个元素的尺寸发生了变化，则需要重新计算渲染树，重新渲染。

## 断开连接
***
当数据传送完毕，需要断开TCP连接，此时发起TCP四次挥手
![https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPuy148fP1xXlNck0YG2BCrEGFdrkfNVWmap2on1mUleNZYaqh53yyzw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/12mPmHVcSumplAiaC2NW3oNc1KawG3jXPuy148fP1xXlNck0YG2BCrEGFdrkfNVWmap2on1mUleNZYaqh53yyzw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

* 发起方向被动房发送报文，Fin,Ack,Seq,表示已经没有数据传输了。并进入到FIN_WAIT_1状态(第一次挥手，由浏览器发起，发送给服务器，我请求报文发送完了，你准备关闭吧)
* 被动方发送报文，Ack,Seq，表示同意关闭请求，此时主机发起方进入FIN_WAIT_2状态。(第二次挥手，由服务器发起，告诉浏览器，我请求报文接受完了，我准备关闭了，你也准备吧)
* 被动方发送报文段，Fin,Ack,Seq,请求关闭连接，并进入LAST_ACK阶段。(第三次挥手，由服务器发起，告诉浏览器，我响应报文发送完了，你准备关闭吧)
* 发起方发送报文段,Ack,Seq.然后进入等待TIME_WAIT状态。被动方收到发起方的报文段后关闭连接。发起方等待一定时间未收到回复，则正常关闭(第一次挥手，由浏览器发起，告诉服务器，我响应报文接受完了。我准备关闭了，你也准备关闭吧)