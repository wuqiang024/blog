正常理解来说，Node.js是应用于服务端，后端的。
但是通过第三方模块`Browserify`也可以使NodeJS中编写的代码，能运行于客户端，包括require()方法组织的代码。

# Browserify
Browserify是一个将NodeJS代码进行打包，，以使之能在浏览器环境使用的打包工具。
main.js代码:

```js
var abc = require('./abc.js');
document.getElementById('result').innerHTML = abc(100, 200);
```

abc.js代码

```js
module.exports = function abc(a, b) {
	return a + b;
}
```
这样的两个文件代码，显然是无法在浏览器中运行的，但是如果经过Browserify，则会变得可以。
再准备一个文件: browserify.js。

```js
var browserify = require('browserify');

var b = browserify();
b.add('./main.js');
b.bundle().pipe(process.stdout);
```

准备好这三个文件，就可以进行本例的打包了。

1、首先安装browserify模块:

2、node browserify进行打包

打包后输出了打包代码，因为上文我们是通过process.stdout输出到命令行的。可以这样运行，将结果输出到bundle.js文件。

```sh
node browserify > bundle.js
```

```html
<html>
<body>
	<div id="result"></div>
<script src="bundle.js"></script>
</body>
</html>
```

可以看到，网页中显示300，正是我们前面Nodejs程序的运行结果。

# Browserify的另一种方法
上面，我们是通过调用browserify模块实现的打包。
如果将browserify通过全局安装，使用命令打包则会更方便些。

```sh
npm install -g browserify
browserify main.js > bundle.js
```