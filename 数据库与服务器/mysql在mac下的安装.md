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