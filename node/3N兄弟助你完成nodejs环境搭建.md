<!--
 * @Author: wuqiang
 * @Date: 2022-03-09 10:08:10
 * @LastEditors: wuqiang
 * @LastEditTime: 2022-06-12 00:51:03
-->
社区有n、nvm、nvs三种方法来对Node.js的版本进行管理，使用起来也很方便，因此称为3N。

# 前言
Node.js是支持跨平台的，Linux、Unix、MacOS等主流一操作系统都是支持的，但是推荐大家使用Linux或者MacOS平台，一方面我们的代码将来投入到生产环境也是基于Linux的，另一方面Windows总是产生一切奇怪的问题。Window环境可以自己搭建一个虚拟机。

# 切换bash
切换到bash
```
chsh -s /bin/bash
```
切换到zsh
```
chsh -s /bin/zsh
```

# nvm
https://blog.csdn.net/zm_miner/article/details/122449762?spm=1001.2014.3001.5502

## 通过curl安装
Github地址https://github.com/nvm-sh/nvm
```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
```

如果安装失败，打开网站: https://www.ipaddress.com/
查询一下 raw.githubusercontent.com对应的IP 地址
再修改/etc/hosts文件，加上其中一个ip地址

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

## 通过wget安装
```
brew install libunistring
brew install openssl@1.1
brew install wget

重点：报错提示缺少啥，就安装啥，最后就安装成功
```
安装步骤:
* 安装nvm: wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
* 查看所有Node.js版本: nvm ls-remote
* 查看本地Node.js版本: nmv ls
* 安装Node.js: nvm install v6.9.5
* 设置系统默认的Node.js版本: nvm alias default v6.9.5

# n
n模块是由TJ大神所编写的。
安装步骤:
* curl -L https://git.io/n-install | bash 或者 npm install -g n # 安装模块 n
* n 12 安装指定版本

常用命令:
* n latest # 安装最新版本
* n lts # 安装稳定版本
* n rm 8.16.0 12.8.0 # 删除一些版本

# nvs
nvs是一个跨平台的Node.js版本管理工具，本身也是基于JS进行开发的。
在执行以下命令之前，需要先安装git

```sh
export NVS_HOME="$HOME/.nvs"
git clone https://github.com/jasongin/nvs "$NVS_HOME"
. "$NVS_HOME/nvs.sh" install
```

常用命令:
* nvs ls # 列出本地所有版本
* nvs ls-remote # 列出Node.js可供下载的版本
* nvs add <version> # 下载一个指定版本
* nvs use [version] # 在当前shell中指定版本。