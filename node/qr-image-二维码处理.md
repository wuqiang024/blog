## 安装
***

```bash
npm install qr-image -S
```

## 用法
***

```javascript
let qr = require('qr-image');
let text = 'http://www.sohu.com';
try {
	let img = qr.image(text, {size: 10});
	res.status(200);
	res.type('image/png');
	img.pipe(res);
} catch(e) {
	res.end('test');
}
```

