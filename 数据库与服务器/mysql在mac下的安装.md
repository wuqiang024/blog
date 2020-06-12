# 安装
打开网址`https://www.mysql.com，点击download后跳转到下载页选择Community选。
选择跟系统版本匹配的mysql版本
此时会要求你注册或者登陆。忽略，选中最下方的`No thanks,just start my download`即可。
在安装界面上一路继续，最后就安装成功了.

# 环境变量
第一步: 在终端切换到根目录，编辑./.bash_profile文件
```sh
cd ~
vim ./.bash_profile
```

第二步: 进入vim编辑环境。按下i进入insert模式，输入
```sh
export PATH=$PATH:usr/local/mysql/bin
export PATH=$PATH:usr/local/mysql/support-files
```

第三步: 按下esc退出insert模式，输入:wq保存配置文件。
```sh
:wq
```

第四步: 在终端界面下输入以下命令，让配置文件的修改生效，并查看环境变量是否设置成功。
```sh
source ~/.bash_profile
echo $PATH
```

# MySQL服务的启动和状态的查看
```sh
// 停止服务
sudo mysql.server stop

// 重启MySQL服务
sudo mysql.server restart

// 查看状态
sudo mysql.server status
```

# 启动
第一步，在终端下输入
```sh
sudo mysql.server start
```

第二步: 启动mysql服务，启动成功后继续输入
```sh
mysql -u root -p
```

第三步: 输入密码后，进入数据库

# 初始化设置
设置初始化密码，进入数据库mysql数据库后执行下面的语句，设置当前root用户的密码为root。
```sh
set password = password('root');
```

# 退出sql界面
```sh
exit
```

# 配置
进入到/usr/local/mysql/support-files目录。里面有个文件:my-default.cnf
将其复制到桌面上，改名为my.cnf，将内容替换为。
```sh
[mysqld]
default-storage-engine=INNODB
character-set-server=utf8
port=3306

[client]
default-character-set=utf8
```
将修改后的文件my.cnf复制到/etc目录下。

重启mysql

`重点来了`:
如果support-files文件夹下面有my-default.cnf或my.cnf文件，则直接打开，
在[mysqld]下面添加`default-character-set=utf8`默认字符集为utf8
init_connect='SET NAMES utf8'(设定链接mysql数据库时使用utf8编码)
在[client]下添加
default-character-set=utf8默认字符集为utf8
如果support-files文件夹下面没有my-default.cnf或my.cnf文件，那么就要在/etc下新建my.cnf

# 检测修改成功
```sh
mysql >>> show variables like '%char%';
```
此数据库就可以愉快的使用了。

# Mac的mysql无法启动的原因
## 一、由于Mac OS X的升级或其他原因可能会导致一个错误:
`Warning:The /usr/local/mysql/data directory is not owned by the 'mysql' or '_mysql'`
原因是某种情况下导致`/usr/local/mysql/data`的拥有者发生了改变，所以只要将其拥有者修改为'mysql'就可以了。
`sudo chown -R mysql /usr/local/mysql/data `

## 二、wheel是什么，引用网上的一段描述如下:
在linux中wheel组就类似于一个管理员的组。
通常在linux下，即使我们有系统管理员root的权限，也不推荐用root用户登录。一般情况下用普通用户登录就可以了，在需要root权限执行一些操作时，再su登录为root用户。但是，任何人只要知道了root密码，都可以通过su命令来登录为root用户。这无疑为系统带来了安全隐患。所以，将普通用户加入到wheel组，被加入的这个普通用户就成了管理员组内的用户，但如果不对一些相关的配置文件进行配置，这个管理员组内的用户与普通用户也就没什么区别。就像警察下班后，没有带枪，穿着便衣和普通人一样，虽然他的的确确是警察。
根据应用的实例不同应用wheel组的方法也不同，这里对于服务器来说，我们希望的是剥夺被加入到wheel组用户以外的普通用户通过su命令来登录为root的机会(只有属于wheel组的用户才可以su登录为root)。这样就进一步增强了系统的安全性。

## 三、查看用户组命令
cat /ect/group | grep [group_name]

# 如果mysql启动不成功，还可能是存在mysql进程
通过`ps -ef | grep mysqld`来查看系统中的mysql进程，然后通过`kill -9 进程ID`来杀掉进程。

`注意的点:`
一、安装的时候最后生成的密码一定要保存好
二、启动的时候报错，记得要执行sudo chown -R mysql:mysql /usr/local/mysql/data/* 或者 sudo chown -R mysql /usr/loca/mysql/data
三、配置环境变量的时候，不要去修改别的地方，否则可能会导致别的应用程序启动失败。