Helmet是一个用来设置一些HTTP响应头的，具有13个中间件方法的集合。
首先，通过`npm install helmet -S`安装helmet包。接下来，在express的入口文件:

```javascript
const express = require('express');
const helmet = require('helmet');

const app = express();

app.use(helmet());
```

最好是尽可能早的在你的入口文件使用helmet以保证响应头的设置。
你也可以单独的只使用其中的某部分功能。比如:

```javascript
app.use(helmet.noCache());
app.use(helmet.frameguard())
```

你可以禁用其中的某一部分中间件，同时不影响其他中间件的使用

```javascript
app.use(helmet({
	frameguard: false
}))
```

如果你使用的还是express3版本，需要确保这些中间件在路由之前使用。