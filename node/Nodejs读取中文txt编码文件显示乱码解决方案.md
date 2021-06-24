Window下默认的编码格式是ASNI，其实这并不是真正的编码格式，但是node.js默认的编码，解码则是目前通用的utf-8，因此在读取windows默认的txt文件时会显示乱码。

```js
const fs = require('fs');
fs.readFile('readme.txt', function(err, data) {
    console.log(data.toString());
})
```

想要解决这个问题，则可通过将txt文件另存为utf-8来解决，或者安装编码解码模块。

`iconv-lite`是由js编写的，没有任何依赖的一个库，支持众多格式的编码和解码。比如上文的txt文件，则可用iconv-lite来用gbk解码。

```js
const fs = require('fs');
const iconv = require('iconv-lite');

fs.readFile('readme.txt', function(err, data) {
    console.log(iconv.decode(data, 'gbk'));
})
```