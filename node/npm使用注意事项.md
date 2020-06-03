# npm使用注意事项

## npm init
使用`npm init`初始化一个空项目是一个好的习惯，即使你对package.json及其他属性非常熟悉，`npm init`也是你开始写新的Node.js应用或模块的一个快捷的办法。`npm init`有智能的默认选项，比如从根目录名称推断模块名称，通过`~/.npmrc`读取你的信息，使用你的git设置来确认repository等。

## npm install
`npm install`是我们常用的命令之一，终端输入`npm install -h`查看使用方法。

![https://github.com/nswbmw/N-blog/raw/master/book/img/2.6.1.png](https://github.com/nswbmw/N-blog/raw/master/book/img/2.6.1.png)

可以看出：我们通过npm install 可以安装npm 上发布的某个版本，某个tag，某个版本区间的模块，甚至可以安装本地目录，压缩包和git/github的库作为依赖。

`小提示: npm i 是 npm install的简写`

直接使用`npm i`安装的模块是不会写入package.json的dependencies或devDependencies的，需要额外加个参数。

`npm install express --save`
`npm install express -S`
安装express，同时将"express":"^4.14.0" 写入dependencies

`npm install express --save-dev`
`npm install express -D`
安装express，同时将"express":"^4.14.0" 写入devDependencies

`npm install express --save --save-exact`
安装express，同时将"express":"4.14.10"写入dependencies

第三种方式将固定版本号写入dependencies，建议线上的Node.js应用都采用这种锁定版本号的方式，因为你不可能保证第三方模块下个小版本是没有验证bug的，即使是很流行的模块。拿Mongoose来说,Mongoose4.1.4引入了一个bug导致调用一个文档entry的remove会删除整个集合的文档。

运行以下命令

```sh
npm config set save-exact true
```
这样每次 npm i xxx --save的时候会锁定依赖的版本，相当于加了`--save-exact`参数

`小提示: npm config set 命令将配置写到了~/.npmrc文件，运行npm config list查看。`

## npm scripts
`npm start`等价于`npm run start`
`npm test` 等价于 `npm run test`

## npm shrinkwrap
前面说过要锁定依赖的版本，但这不能完全防止意外的发生，因为锁定的只是最外一层的依赖，而里层依赖的模块的package.json有可能写的是"mongoose":"*"。为了彻底锁定依赖的版本，让你的应用在任何机器上都是同样的模块(不管嵌套多少层)，通过 npm shrinkwrap，会在当前目录下产生一个`npm-shrinkwrap.json`，里面包含了通过node_modules计算出的模块的依赖树及版本。上面的截图也显示：只要目录下有npm shrinkwrap.json则运行npm install的时候会优先使用npm-shrinkwrap.json进行安装，没有则使用package.json进行安装。