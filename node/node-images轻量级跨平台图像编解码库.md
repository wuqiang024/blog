# Node.js轻量级跨平台图像编解码库
```js
const images = require('images');

images('input.jpg')  // load image from file
	.size(400)	// 等比缩放图像到400像素宽
	.draw(images('logo.png'), 10, 10)  // 在(10, 10)处绘制logo
	.save('output.jpg', {
		quality: 50
	});  // 保存图片到文件，图片质量为50
```

# 安装
```sh
npm install images
```

# API接口
node-images提供了类似jQuery的链式调用API,你可以这样开始:

```js
// 从指定文件加载并解码图像
images(file)

// 创建一个指定高宽的透明图像
images(width, height)

// 从buffer数据中解码图像
images(buffer[, start[, end]])

// 从另一个图像中复制区域来创建图像
images(image[, x, y, width, height])

images.fill(red, green, blue[, alpha])
// eg: images(200,100).fill(0xff,0x00,0x00,0.5) 用颜色填充图像

images.gc() // 强制调用v8的垃圾回收机制

images.getUsedMemory() // 得到图像处理库占用的内存大小
