## 安装
***
```bash
npm install express-interceptor -S
```

## 使用
***

```javascript
const express = require('express');
const cheerio = require('cheerio');
const interceptor = require('express-interceptor');

const app = express();

const paragraphInterceptor = interceptor(function(req, res) {
	return {
		isInterceptable: function(){
			return /text\/html/.test(res.get('Content-Type'));
		},
		intercept: function(body, send) {
			var $document = cheerio.load(body);
			$document('body').append('<p>test</p>');
			send($document.html)
		}
	}
});

app.use(paragraphInterceptor);
app.use(express.static(path.join(__dirname, 'public')));
app.listen(3000);
```