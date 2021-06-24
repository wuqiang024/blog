# npx使用教程
***
npm从5.2版本开始，增加了npx命令，他有很多用处，本文介绍该命令的主要使用场景。
Node自带npm模块，所以可以直接使用npx命令，万一不能用，就要手动安装一下。

```js
npm install npx -g
```

## 调用项目安装的模块
***
npx想要解决的问题，就是调用项目内部安装的模块，比如，项目内部安装了测试工具`Mocha`。
```js
npm install -D mocha
```

一般来说，调用Mocha，只能在项目脚本和package.json的`scripts`字段里面，如果想在命令行下调用，必须像下面这样。
```js
// 项目根目录下执行
node-modules/.bin/mocha --version
```

npx就是想解决这个问题，让项目内部安装的模块用起来方便，只要像下面这样调用就行了。
```js
npx mocha --version
```

npx的原理很简单，就是运行的时候，会到`node_modules/.bin`路径和环境变量`$PATH`里头，检查命令是否存在。
由于npx会检查环境变量$PATH，所以系统命令也可以调用。

```js
npx ls
```

## 避免全局安装模块
***
除了调用项目内部模块，npx还能避免全局安装的模块，比如,`create-react-app`这个模块是全局安装，npx可以运行它，而不进行全局安装。
```js
npx creat-react-app my-react-app
```

上面代码运行时，npx将`create-react-app`下载到一个临时目录，使用以后再删除。所以，以后再次执行上面的命令，会重新下载`create-react-app`。
下载全局模块时，npx允许指定版本。
```js
npx uglify-js@3.1.0 main.js -o ./dist/main.js
```
上面代码指定使用3.1.0版本的`uglify-js`压缩脚本。

注意，只要npx后面的模块无法在本地发现，就会下载同名模块，比如本地没有安装`http-server`模块，下面的命令就会自动下载该模块，在当前目录启动一个web服务。
```js
npx http-server
```

## --no-install参数和--ignore-existing参数
***
如果想让npx强制使用本地模块，不下载远程模块，可以使用`--no-install`参数，如果本地不存在该模块，就会报错。
```js
npx --no-install http-server
```

反过来，如果忽略本地的同名模块，强制安装使用远程模块，可以使用`--ignore-existing`参数。比如，本地以及安装了`create-react-app`，但是还是想使用远程模块，就使用这个参数。
```js
npx --ignore-existing create-react-app my-react-app
```

## 使用不同版本的node
***
利用npx可以下载模块这个特点，可以指定某个版本的Node运行脚本，他的窍门就是使用npm的node模块。
```js
npx node@0.12.8 -v
```
上面命令会使用0.12.8版本的Node脚本执行命令。原理是从npm下载这个版本的node,使用后再删掉。
某些场景下，这个方法用来切换node版本。比nvm那样的版本管理器方便一些。

## -p参数
***
`-p`参数用于指定npx所要安装的模块。所以上一节的命令可以写成下面这样。
```js
npx -p node@0.12.8 node -v
```
上面命令指定先安装`node@0.12.8`，然后再执行`node -v`命令。
`-p`参数对于需要安装多个模块的场景很有用。
```js
npx -p lolcatjs -p cowsay [command]
```

## -c参数
***
如果npx安装多个模块，默认情况下，所执行的命令中，只有第一个可执行项会使用npx安装的模块，后面的可执行项还是会交给shell解释。
```js
npx -p lolcatjs -p cowsay 'cowsay hello | lolcatjs`
```
上面代码中，`cowsay hello | lolcatjs`执行时会报错，原因是第一项`cowsay`由npx解释，而第二项命令`lolcatjs`由shell解释，但是lolcatsjs并没有全局安装，所以报错。
`-c`参数可以将所有命令都用npx解释，有了它，下面代码就可以正常执行了。
```js
npx -p lolcatjs -p cowsay -c 'cowsay hello | lolcatjs'
```

`-c`参数的另一个作用，是将环境变量带入所要执行的命令。举例来说，npm提供当前项目的一些环境变量，可以用下面的命令查看。
`npm run dev | grep npm_`
`-c`参数可以把这些npm的环境变量带入npx命令。
`npx -c 'echo "$npm_package_name"'`
上面代码会输出当前项目的项目名。

## 执行GitHub源码
***
```js
// 执行Gist代码
npx https://gist.github.com/zkat/4bc19503fe9e9309e2bfaa2c58074d32

// 执行仓库代码
npx github:piuccio/cowsay hello
```
注意，远程代码必须是一个模块，即必须包含`package.json`和入口脚本。