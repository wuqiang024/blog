##  基本使用
***

```
npm install svg-captcha
yarn add svg-captcha
```

创建普通验证码

```
const svgCaptcha = require('svg-captcha');
const cap = svg.create();
console.log(cap);
```

调用create()以后，会返回一个对象，结构如下: {data:'', text:'' }。

* data: 验证码 svg 图片
* text: 验证码字符

create()的参数如下:

* size: 4  //验证码长度
* ignoreChars: '0oi1'  // 验证码字符中排除o0i1
* noise: 2  // 干扰线条的数量
* color: true  // 验证码的字符是否有颜色，默认没有，如果设定了背景，则默认有
* background: '#cc9966'  // 验证码图片背景色

`创建算数式验证码`

```
cosnt cap = svgCaptcha.createMathExpr(options)
```

## 在express中使用
***

```
const express = require('express');
const captcha = require('svg-captcha');
const router = express.Router();

router.get('/', (req, res)=>{
	const cap = captcha.createMathExpr();
	req.session.captcha = cap.text;
	res.type('svg');
	res.send(cap.data);
})
```

## 前端使用
***

```
<img src="/captcha" onclick={$(event.target).attr('src', '/captcha?'+Math.random())}>
```