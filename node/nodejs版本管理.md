# Ubuntu使用n进行版本管理
## 安装n模块
```sh
npm install -g n
```

## 用法
### 清楚npm缓存
```sh
npm cache clean -f
```

### 安装最新版本node
```sh
n latest # 安装最新版本
n stable # 安装最新的稳定版
n 6.9.0 # 安装指定版本
n lts # 安装最新的LTS版本
```

### 查看所有版本node
```sh
n ls
```

### 删除本地指定版本node
```sh
n rm 版本号
```

### 安装npn最新版本
```sh
npm update npm -g
```

## 直接启动不同版本的Node
加入我们将默认的Node版本设置为6.10.0了，而我们要使用7.6.0启动某个应用，也非常简单，只需要:
```sh
n use 7.6.0 index.js
```
这个功能可以用来不需要babel，直接使用高版本node支持一些高级属性

最后，我们可以创建一个快捷的命令:
```sh
echo alias node7 = "\" n use 7.6.0 --harmony-async-await\"" >> ~/.bashrc
source ~/.bashrc
```
这样我们就可以愉快的使用node v7.x.x运行我们的Js了
```sh
node7 async.js
```

# 使用nvs管理本地node版本
## 使用场景
一般来说，直接从Node.js官网下载对应安装包即可完成环境配置
但在本地开发的时候，经常需要快速更新或更换版本。
社区有nvm, n等方案，我们推荐跨平台的nvs。
nvs是跨平台的，nvs本身是基于Node编写的，我们可以参与维护。

## 安装
Linux/macOS环境
通过git clone对应的项目即可。

```sh
export NVS_HOME = '$HOME/.nvs'
git clone https://github.com/jasongin/nvs --depth=1 "$NVS_HOME"
. "$NVS_HOME/nvs.sh" install
```

windows的话建议还是使用msi文件完成初始化工作。
访问nvs/releases下载最新版本的nvs.msi，然后双击安装即可。

配置镜像地址

```sh
nvs remote node https://npm.taobao.org/mirrors/node/
nvs remote
```

## 使用指南
通过以下命令，即可非常简单的安装Node.js的最新LTS版本


```sh
# 安装最新的LTS版本
nvs add lst

# 配置为默认版本
nvs link lts

# 安装其他版本
nvs add 8

# 查看已经安装的版本
nvs ls

# 在当前shell 切换版本
nvs use 8
```

## 共用npm全局模块
使用nvs上，默认的prefix是当前激活的Node.js版本的安装路径
带来一个问题是:切换版本后，之前安装的全局命令模块需要重新安装，非常不方便。
解决方案是配置统一的全局模块安装路径到`~/.npm-global`，如下:

```sh
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
```

还需要配置环境变量到`~/.bashrc`或`~/.zshrc`文件里面:

```sh
echo "export PATH=~/.npm-global/bin:$PATH" >> ~/.zshrc
source ~/.zshrc
```
