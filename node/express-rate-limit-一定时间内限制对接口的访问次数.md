## 安装
***

```bash
npm install express-rate-limit -S
```

## 用法
***

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
	windowMs: 15 * 60 * 1000,  // 15 minutes
	max: 100 // limit each IP to 100 requests per window
})

app.use(limiter);
app.use('/api/', limiter); // 只对 api 前缀的接口使用

const createLimiter = rateLimit({
	windowMs: 60 * 60 * 1000,
	max: 5,
	message: 'Too many accounts created from this IP, please try again after a hour'
});

app.post('/create-account', createLimiter, function(req, res) {
	
})