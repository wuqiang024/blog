如果没有提供编码格式，文件操作及很多网络操作就会将数据作为Buffer类型返回。

# toString
默认转为`UTF-8`格式，还支持`ascii`、'base64'。

# data URI
```js
// 生成data URI
const fs = require('fs');
const mime = 'image/png';
const encoding = 'base64';
const base64Data = fs.readFileSync(`${__dirname}/monkey.png`).toString(encoding);
const uri = `data:${mime};${encoding},${base64Data}`;
console.log(uri);
```

```js
// data URI 转文件
const fs = require('fs');
const uri = "data:image/png;base64Data,viQWds...";
const base64Data = url.split(',')[1];
const buf = Buffer(base64Data, 'base64');
fs.writeFileSync(`${__dirname}/second.png`, buf);
```
