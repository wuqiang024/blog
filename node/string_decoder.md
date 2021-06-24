## 模块介绍
***

string_decoder 模块用于将Buffer转成对应的字符串。使用者通过调用stringDecoder.write(buffer)，可以获得buffer对应的字符串。
它的特殊之处在于，当传入的buffer不完整(比如三个字节的字符，只传了2个)，内部会维护一个internal buffer将不完整的字节cache住，等到使用者再次调用stringDecoder.write(buffer)传入剩余字节，来拼成完整的字符。

这样可以有效避免buffer不完整带来的错误，对于很多场景，比如网络请求中的包解析等，非常有用。


## 入门例子
***

这节分别演示了decode.write(buffer)、decode.end([buffer])两个主要API的用法。

例子一:

decoder.write(buffer)调用传入了Buffer对象，相应的返回来对应的字符串;

```javascript
const StringDecoder = require('string_decoder').StringDecoder;
const decoder = new StringDecoder('utf8');

const str = decoder.write(Buffer.from(...));
console.log(str);
```

例子二:

当decoder.end([buffer])被调用时，内部剩余的buffer会被一次性返回。如果此时带上buffer参数，那么相当于同时调用decoder.write(buffer)和decoder.end()。

```javascript
const StringDecoder = require('string_decoder').StringDecoder;
const decoder = new StringDecoder('utf8');

let str = decoder.write(Buffer.from([]));

str = decoder.end(Buffer.from([]))
```

## 例子: 分多次写入多个字节
***

下面的例子，演示了分多次写入多个字节时，string_decoder模块是怎么处理的。
首先，传入了<Buffer e4 bd a0 e5 a5>, 好 还差一个字节，此时，decoder.write(xx)返回`你`。
然后，再次调用decoder.write(Buffer.from([0xbd])), 将剩余的1个字节传入，成功返回`好`。

```javascript
const StringDecoder = require('string_decoder').StringDecoder;
const decoder = new StringDecoder('utf8');

let str = decoder.write(Buffer.from([0xe4, 0xbd, 0xa0, 0xa5]));
console.log(str);  // 你

str = decoder.write(Buffer.from([0xbd]));
console.log(str);  // 好
````

例子: decoder.end()时，字节数不完整的处理
***

decoder.end(buffer)时，仅传入了`好`的第一个字节，此时调用了decoder.end()，返回一个不可识别字符。

```javascript
const StringDecoder = require('string_decoder').StringDecoder;
const decoder = new StringDecoder('utf8');

let str = decoder.end(Buffer.from([0xe5]));
console.log(str);
console.log(Buffer.from(str));
```
官方文档对于这种情况的解释是这样的，大约是约定成俗了，当utf8码点无效时，替换成 ef bf bd；