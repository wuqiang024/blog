# 远程开发配置
下面开始详细讲一下vscode远程开发的配置

## 第一步: 安装插件
配置远程开发首先需要安装一个名为`Remote Development`的插件，具体操作步骤如下
* 点击扩展按钮
* 搜索`Remote Development`
* 安装

## 第二步: 配置远程服务器
安装之后，点击远程资源管理器，在SSH TARGETS配置远程服务器，具体步骤如下.
* 点击齿轮图标
* 打开弹出的config文件
* 分别配置Host,Hostname,User
这里需要注意一个，Host是一个名称，自己可以随意命名。Hostname是远程服务器的IP，User是用于登录远程服务器的账号名称。

## 第三步: 修改设置
把鼠标fan股灾上一步配置的远程连接条目上，点击Connect to Host in New Window,然后就会在新的窗口打开我们想要的远程连接。

## 配置免密登录
由于vs code是通过ssh远程连接到服务器的方式进行远程开发，因此，每次打开远程连接时都会提示输入密码，我们可以通过配置免密登录的方式避免每次连接时都需要重复输入密码。

## 第一步: 生成windows公钥
这个需要windows配置有ssh工具，可以通过安装git,openssh实现
打开cmd
```
ssh-keygen
```
然后一直点击Enter键，不用输入任何内容，最后会在C:\Users\user_name\.ssh路径下生成公钥文件，可以看到有一个id_rsa.pub文件，然后通过FTP等方式把这个文件上传到远程服务器

## 第二步: 配置远程服务器
进入SSH配置目录
```
cd ~/.ssh
ls
```
查看一下是否有一个名为authorized_keys的文件，如果没有创建一个，然后把刚上传的id_rsa.pub中的内容附到authorized_keys文件中。
```
touch authorized_keys
cat ~/id_rsa.pub >> authorized_keys
```

## 第三步: 修改文件权限
这一步非常重要，如果没有这一步，前面的操作都没用。就是给authorized_keys修改为600的权限。
```
chmod -R 600 authorized_keys
```
这样就完成了免密登录的设置