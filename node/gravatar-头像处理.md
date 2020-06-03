## 安装
***

```bash
cnpm install gravatar
```

## 用法
***

```javascript
var gravatar = require('gravatar');

gravatar.url(email);
gravatar.url(email, options);
gravatar.url(email, options, protocol);

gravatar.profile_url(email);
gravatar.profile_url(email, options);
gravatar.profile_url(email, options, protocol);
```

## 参数
***

* email: 头像email地址
* options: 参数:
`size = s; default = d; forcedefault = f;  protocol = 'http' or 'https'`
`format 只针对profile_url。参数为 'xml', 'qr', 默认是 'json'`


* size或者s 是大小的意思，r是等级，参数一般是g, d有几个选项
** 404: 找不到跟邮件地址关联的头像时，会返回默认头像，一般是个灰度图
** mm: 一个简单的卡通样式的轮廓背景图
** identicon: 基于email哈希值的几何样式图
** monsterid: 具有不同颜色，脸型等的怪兽
** retro: 比特像素图
** blank: 透明的png图