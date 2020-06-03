# path(路径)
path模块主要用来对文件路径进行处理，比如提取路径，后缀，拼接路径等。

## path的使用
`代码示例: /lession12/path.js`
```js
const path = require('path');
const str = '/root/a/b/1.txt';

console.log(path.dirname(str)) // 获取文件目录: /root/a/b
console.log(path.basename(str)) // 获取文件名: 1.txt
console.log(path.extname(str)) // 获取文件后缀: .txt
console.log(path.resolve(str, '../c', 'build', 'strict')) 
// 将路径解析为绝对路径: c:\root\a\b\c\build\strict
// path.resove相当于将所列出的路径用cd命令符轮询一遍
console.log(path.resolve(str, '../c', 'build', 'strict', '../..', 'assets')) // \root\a\b\c\assets
console.log(path.resolve(path.dirname, 'build')) // 将路径解析为绝对路径: c:\projects\nodejs....
```

`值得一提的是path.resolve方法，它可以接收任意个参数，然后根据每个路径参数之间的关系，将路径最终解析为一个绝对路径。`

`__dirname指的是当前模块所在的绝对路径名称，它的值会自动根据当前的绝对路径变化，等同于path.dirname(__filename)的结果。`

说明: `__dirname`、`__filename`总是返回文件的绝对路径。

`process.cwd()`总是返回node命令所在的文件夹。

* path.parse 用于解析当前路径为一个json格式的数据
* path.format相当于格式化json数据为一个字符串