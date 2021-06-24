##实现思路
1、读取图片二进制数据
2、转成base64字符串
3、转成datauri
而datauri的格式如下
data:[][;base64]
具体到png图片，大概如下，其中'xxx'就是前面的base64字符串了。
`data:image/png;base64,xxx`

## 具体实现
```
var fs = require('fs');
var filepath = './1.png';
var bData = fs.readFileSync(filepath);
var base64Str = bData.toString('base64');
var datauri = 'data:image/png;base64,' + base64Str;
console.log(datauri);
```