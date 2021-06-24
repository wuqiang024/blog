## 安装
***

```bash
npm install serve-favicon
```

## 用法
***

```javascript
var express = require('express');
var favicon = require('serve-favicon');
var path = require('path');
var app = express();

app.use(favicon(path.join(__dirname, 'pubulic', 'favicon.ico')));

app.listen(3000);
```