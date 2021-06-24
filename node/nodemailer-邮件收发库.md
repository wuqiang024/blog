## 安装
***

```bash
npm install nodemailer -S
```

## 使用NodeMailer发送邮件

```javascript
var nodemailer = require('nodemailer');
var transporter = nodemailer.createTransport({
	service: 'Gmail',
	// secureConnection: true, // 使用SSL方式(安全方式，防止被窃取信息)
	auth: {
		user: 'xxx@gmail.com',
		pass: 'xxxx'
	}
});

var mailOptions = {
	from: 'bass',
	to: 'xxx@xx.com',
	subject: 'hello',
	text: 'hello world',
	html: '<b>hello world</b>'
}

transporter.sendMail(mailOptions, function(err, info) {
	if(err) {
		console.log(err);
	} else {
		console.log(info.response);
	}
})
```

邮件服务并不是实时的，有时候会稍微慢一点。可能会有几分钟的延迟。


## 发邮件的高级使用

Nodemailer提供的，发邮件的高级功能包括:
1. CC和BCC
2. 发送附件
3. 发送HTML格式内容，并嵌入图片
4. 使用安全的SSL通道

### CC和BCC
发送邮件时选收件人，有3个选项，TO, CC, BCC。
* TO: 是收件人
* CC: 是抄送，用于通知相关的人，收件人可以看到都邮件抄送给谁了。
* BCC: 是密送，也是用于通知相关的人，但是收件人看不到邮件被密送给谁了。

```javascript
var mailOptions = {
	from: 'from@163.com',
	to: 'to@163.com',
	cc: 'cc@163.com',
	bcc: 'bcc@163.com',
	subject: 'subject',
	text: 'text',
	html: 'html'	
}
```

### 发送附件
发送附件也是邮件系统常用的功能，Nodemailer支持多种邮件附件。接下来测试发送两个文件作为附件

```javascript
var mailOptions = {
	from: 'from@163.com',
	to: 'to@163.cc@163.com',
	subject: 'subject',
	text: 'text',
	html: '<b>html</b>',
	cc: 'cc@163.com',
	bcc: 'bcc@163.com',
	attachments: [
		{
			filename: 'text0.txt',
			content: 'hello world'
		},
		{
			filename: 'text1.txt',
			path: './attach/text1.txt'
		}
	]
}
```

### 发送HTML格式内容，并嵌入图片
Nodemailer也为我们提供了在HTML文件中嵌入图片的功能，程序中只要配置cid，作为图片的唯一引用地址就行了。上传本地图片，设置cid为0000001，然后在html中，img的src属性指向000001的cid就行了。
代码如下:

```javascript
var mailOptions = {
	...,
	html: '<b>hello world</b><br/>embeded image: <img src="cid:000001"/>',
	attachments: [
		filename: '01.jpg',
		path: './img/r-book1.jpg',
		cid: '000001'
	]
}
```

### 使用安全的SSL通道
为了邮件正文内容的安全性，我们通常会加密发送，防止邮件在网络传输过程中，明文被路由的中间服务器所截获。大部分的邮件服务商都支持SSL的加密通道。
Gmail的SSL发送设置，要新建一个transporter，配置端口为465，secureConnection属性为true，可以参考以下代码:

```javascript
var stransporter = nodemailer.createTransport({
	service: 'Gmail',
	secureConnection: true,
	port: 465,
	auth: {
		user: 'user@gmail.com',
		pass: 'xxxxxx'
	}
})

stransporter.sendMail(mailOptions, function(err, info){})
```	