包管理器又叫软件包管理系统，他是在电脑中自动安装，配置，卸载和升级软件包的工具组合。
每个工具或者开发语言都有相应的包管理器，好比Ubuntu的apt-get,centos的yum,java的Maven仓库等。
Node.js中最出名的包管理器为NPM，也是生态最好的。

# 什么是NPM
NPM是Node.js的包管理器。允许我们为Node.js安装各种模块，这个包管理器为我们提供了安装，删除等其他命令来管理模块。这里有一点需要注意，我们必须有一个package.json文件或者node_modules目录安装模块到本地。

NPM最好的一点是他会在本地存储我们所安装的依赖项，存在于package.json的dependencies对象里。例如，如果一个模块X使用了模块A版本为1.0，模块Y使用了模块A版本为1.5，那么模块X或Y都将在本地拥有自己对应的模块A的副本。

# NPM源设置
在国内有时候受限于网络因素的影响，通常在安装一个包管理器之前可以切换为taobao源，速度可以更快，但是注意如果是私有模块在NPM官方的，则必须切换为官方源，否则会出现404错误。

查看当前源: `npm config get registry`

切换为淘宝源: `npm config set registry=https://registry.npm.taobao.org`

切换为npm官方源`(在npm publish)`的时候需要切换为官方源: `npm config set registry=https://registry.npmjs.org`

# NPM注册登录
注册
```sh
npm adduser
Username: your name
Password: your password
Email: (this IS pubulic) your email
```

查看当前使用的用户
```sh
npm whoami
```

npm登录
```sh
npm login
```

# 私有模块
如果是公司团队或者个人项目的私有npm包，进行发布的时候要注意下，模块的名字要以`@`符号开始、`/`符号结束，中间部分为私有包的组织名。
例如: `@may/logger`，may为组织名，logger为包名。

package.json

```js
{
	name: "@may/logger"
}
```

# NPM-Module发布
进入项目根目录，输入命令
```sh
npm publish
```

# 常见问题
## 问题一
`no_perms Private mode enable, only admin can publish this module: coorddistance`
因为网络问题，很多人都把NPM的镜像代理到淘宝或者别的地方了，需要设回原来的镜像。

## 问题二
`Unexpected end of input at 1:3637 npm ERR! egistry.npmjs.org/mkdirp/-/mkdirp-0.3.2.tgz"},"engines":{"node":"*"}`
执行命令 npm cache clean --force

## 问题三
Node项目部署私有包报错404，一般两种情况造成的:
* 检查服务器是否登录npm账号
* 执行命令`npm config get registry`检查是否指向https，没有指向https执行命令`npm config set registry=https://registry.npmjs.org`
