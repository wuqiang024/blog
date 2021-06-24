# Buffer初识
在引入TypedArray之前，Javascript语言没有用于读取或操作二进制数据流的机制，Buffer类是作为Node.js API的一部分引入的，用于在TCP流，文件系统操作，以及其他上下文中与八位字节流进行交互。总结一句话就是：`Node.js可以用来处理二进制数据流或者与之进行交互`。

Buffer 用于读取或操作二进制流，作为Node.js API的一部分使用时无需require，用于操作网络协议、数据库、图片和文件I/O等一些需要大量二进制数据的场景。Buffer在创建时大小已经确定而且是无法调整的，在内存分配这块Buffer是由c++层面提供而不是V8。

## 什么是二进制数据
读到二进制数据我们大脑里可能会浮想到010101这种代码命令。
![https://mmbiz.qpic.cn/mmbiz_jpg/zPkNS9m6iatLx3o3p7BDdmjrdaJ5bZKh0Jl5ZJmNj94VNq96W5DGWsnzRaceAicdyCDyibiceoMvZAkcdm80prGXQw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_jpg/zPkNS9m6iatLx3o3p7BDdmjrdaJ5bZKh0Jl5ZJmNj94VNq96W5DGWsnzRaceAicdyCDyibiceoMvZAkcdm80prGXQw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

正如上图所示，二进制数据是使用0和1两个数码来表示的数据，为了存储或展示一些数据，计算机需要先将浙西数据转换为二进制来表示。例如，我想存储66这个数字，计算机会先将数字66转化为二进制01000010表示，

我们知道数字只是数据类型之一，其他的还有字符串，图像，文件等。例如我们对一个英文M操作，在JS里头通过'M'.charCodeAt()取到对应的ASCII码之后(通过以上的步骤)会转化为二进制表示。

## 什么是Stream
流，英文Stream是对输入输出设备的抽象，这里的设备可以是文件，网络，内存等。
流是有方向的，当程序从某个数据源读入数据，会开启一个输入流，这里的数据源可以是文件或网络，例如我们从a.txt文件读入数据。想法的当我们的程序需要写出数据到指定数据源(文件、网络等)时，则开启一个输出流。当有一些大文件操作时，我们就需要Stream像管道一样，一点一点的将数据流出。

## 举个例子
我们现在又一大罐水需要浇一片菜地，如果我们将水罐的水一下全部倒入菜地，首先需要多么大的力气(这里的力气好比计算机中的硬件性能)才搬得动。如果我们拿了个水管将水一点点的流入我们的菜地，这个时候就不需要费那么大力气就可完成。

## 什么是Buffer
通过以上Stream的讲解，我们已经看到数据是从一端流向另一端，那么他们是如何流动的呢？
通常，数据的移动是为了处理或者读取他，并根据他进行决策。伴随着时间的推移，每一个过程都会有一个最小或最大数据量。如果数据到达的速度比进程消耗的速度快，那么少数早到达的数据会处于等候区等候被处理。反之，如果数据达到的速度比进程消耗的数据慢，那么早先到达的数据需要等待一定量的数据到达后才能被处理。
这里的等待区就指的是缓冲区(Buffer)，他是计算机的一个小物理单位，通常位于计算机的RAM中。

## 公共汽车站乘车例子
举一个公共汽车站乘车的例子，通常公共汽车会每隔几十分钟一趟，在这个时间到达之前就算乘客已经满了，车辆也不会提前发车，早到的乘客就需要先在车站进行等待，假设到达的乘客过多，后到的一部分则需要在公共汽车站等待下一趟车。

上面的等待区公共汽车站，对应到我们的Node.js中就是缓冲区(Buffer)，另外乘客到达的速度使我们不能控制的，我们能控制的也只有何时发送数据。

## Buffer的基本使用
了解了Buffer的一些概念后，我们来看下Buffer的一些基本使用，这里不会猎取所有的API使用，仅列举一部分常用的。

## 创建Buffer
在6.0.0之前的Node.js版本中，Buffer实例是使用Buffer构造函数创建的，该函数根据提供的参数以不同方式分配返回的Buffer `new Buffer()`
现在可以通过Buffer.from()、Buffer.alloc()与Buffer.allocUnsafe()三种方式来创建。

## Buffer.from
```js
const b1 = Buffer.from('10');
const b2 = Buffer.from('10', 'utf-8');
const b3 = Buffer.from([10]);
const b4 = Buffer.from(b3);
```

## Buffer.alloc
返回一个已初始化的Buffer，可以保证新创建的Buffer永远不会包含旧数据。
```js
const b1 = Buffer.alloc(10); // 创建一个大小为10个字节的缓冲区
console.log(b1); // <Buffer 00 00 00 00 00 00 00 00 00 00>
```

## Buffer.allocUnsafe
创建一个大小为size字节的新的未初始化的Buffer，由于Buffer是未初始化的，因此分配的内存片段可能包含敏感的旧数据。在Buffer内容可读的情况下，则可能会泄露他的旧数据，这个是不安全的，使用时需要谨慎。
```js
const b1 = Buffer.allocUnsafe(10);
console.log(b1) // 可能会有数据
```

## Buffer 字符编码

通过使用字符编码可实现Buffer实例与JS字符串之间的相互转换，目前所支持的字符编码如下所示:
* 'ascii'-仅适用于7位ASCII数据。此编码速度很快，如果设置则会剥离高位。
* 'utf8'-多字节编码的Unicode字符。许多网页和其他文档格式都使用UTF-8。
* 'utf16le'-2或4个字节，小端序编码的Unicode字符。支持代理对(U+10000至U+10FFFF)。
* 'ucs2'-'utf16le'的别名
* 'base64'-Base64编码。当从字符串创建Buffer时，此编码也会正确地接受RFC4648第五节中指定的'URL和文件名安全字母'。
* 'latin1'-一种将Buffer编码成单字节编码字符串的方法
* 'binary'-'latin1'的别名
* 'hex'-将每个字节编码成两个十六进制的字符。

```js
const buf = Buffer.from('hello world', 'ascii');
console.log(buf.toString('hex'));
```

## 字符串与Buffer类型转换
### 字符串转Buffer
通过上面讲解的Buffer.from()实现，如果不传递encoding默认按UTF-8格式转换存储。

```js
const buf = Buffer.from('Node.js技术栈', 'UTF-8');
console.log(buf);
console.log(buf.length);
```

## Buffer转换为字符串
Buffer转换为字符串也很简单，使用toString([encoding],[start],[end])方法，默认编码仍为UTF-8，如果不传start、end可实现全部转换，传了start,end可实现部分转换(这里要小心)

```js
const buf = Buffer.from('Node.js 技术栈', 'UTF-8');
console.log(buf);
console.log(buf.length);
console.log(buf.toString('UTF-8',0,9));
```
这里可以看到输出结果有乱码，因为上面示例中默认编码方式为UTF-8，这里一个中文在UTF-8下占用3个字节，而我们设定范围为0-9，因此只输出了8a，这个时候就会造成字符被截断出现乱码。

## Buffer内存机制
在Nodejs中的内存管理和V8垃圾回收机制一节主要讲解了在Node.js的垃圾回收中主要用V8管理，但是并没有提到Buffer类的数据是如何回收的，下面让我们了解Buffer的内存回收机制。
由于Buffer需要处理的是大量的二进制数据，加入用一点就向系统去申请，则会造成频繁的向系统申请内存调用，所以Buffer所占用的内存不再由V8分配，而是在Node.js的C++层面完成申请，在JS中进行内存分配。因此这部分内存我们成为`堆外内存`。

## Buffer内存分配原理
Node.js采用了slab机制进行预先申请，事后分配，是一种动态的管理机制。
使用Buffer.alloc(size)传入一个指定的size就会申请一块固定的内存区域，slab具有如下三种状态:
* full: 完全分配状态
* partial: 部分分配状态
* empty: 没有被分配状态

## 8KB限制
Node.js以8KB为界限来区分是小对象还是大对象，在buffer.js中可以看到以下代码

```js
Buffer.poolSize = 8 * 1023；
```

## Buffer对象分配
以下代码示例，在加载时直接调用了createPool()相当于直接初始化了一个8kb的内存空间，这样在第一次进行内存分配时也会变得更高效。另外在初始化的同时还初始化了一个新的变量poolOffset = 0，这个变量会记录已经使用了多少字节。

```js
Buffer.poolSize = 8 * 1024;
var poolSize, poolOffset, allocPool;

...

function createPool() {
	poolSize = Buffer.poolSize;
	allocPool = createUnsafeArrayBuffer(poolSize);
	poolOffset = 0;
}
createPool();
```

## Buffer内存分配总结
1、在初次加载时就会初始化1个8KB的内存空间
2、根据申请的内存大小分为小Buffer对象和大Buffer对象
3、小Buffer情况，会继续判断这个slab空间是否足够
** 如果空间足够就去使用剩余空间同时更新slab分配状态，偏移量会增加
** 如果空间不足，slab空间不足，就会去创建一个新的slab空间来分配
4、大Buffer情况，则会直接走createUnsafeBuffer(size)函数
5、不论小Buffer对象还是大Buffer对象，内存分配是在c++层面完成，内存管理在JS层面，最终还是可以被V8的垃圾回收标记回收。

## Buffer的一些应用场景
### IO操作
关于I/O可以是文件I/O或网络I/O，以下为通过流的方式将input.txt的信息读取出来之后写入到output.txt文件
```js
const fs = require('fs');
const inputStream = fs.createReadStream('input.txt');
const outputStream = fs.createWriteStream('output.txt');
inputStream.pipe(outputStream);
```
在Stream中我们不需要手动去创建自己的缓冲区，在Node.js的流中将会自动创建。

### zlib.js
zlib.js为node核心库之一，其利用了缓冲区Buffer的功能在操作二进制数据流，提供了压缩和解压功能。

### 加解密
在一些加解密算法中会遇到使用Buffer，例如crypto.createCipheriv的第二个参数key为String或Buffer类型，如果是Buffer类型，就用到了本篇我们讲到的内容，以下做了一个简单的加密示例，重点使用了Buffer.alloc()初始化一个实例，之后使用了fill方法做了填充。

## Buffer VS Cache
`缓冲和缓存的区别`

### 缓冲(Buffer)是用于处理二进制流数据，将数据缓冲起来，他是临时性的，对于流式数据，会采用缓冲区将数据临时存储起来，等缓冲到一定的大小之后再存入硬盘。

### 缓存(Cache)
缓存(Cache)我们可以看做是一个中间层，他可以是永久性的将热点数据进行缓存，使得访问速度更快，例如我们通过Memory，Redis等将数据从硬盘或其他第三方接口中请求过来进行缓存，目的就是将数据存于内存的缓存区中，这样对同一个资源进行访问，速度会更快。
