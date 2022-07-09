<!--
 * @Author: wuqiang
 * @Date: 2022-03-09 10:08:10
 * @LastEditors: wuqiang
 * @LastEditTime: 2022-04-20 16:20:58
-->
## 下载
打开官网https://redis.io/
下载最新稳定版本

## 安装
下载完后打开命令行工具，执行解压命令

```sh
tar xzvf redis-4.0.10.tar.gz
```

将解压后的文件夹放到`/usr/local`

```js
mv /Users/admin/Downloads/redis-4.0.10 /usr/local
cd /usr/local/redis-4.0.10
sudo make test  // 编译测试
sudo make install // 编译安装
redis-server // 启动
```

## Mac OS下的安装
***
```sh
brew --version
brew install redis
brew services start redis
brew services stop redis
```

## 参考文章
***
https://www.cnblogs.com/liyihua/p/14482412.html


## 管理工具
***
redis desktop manager

## redis主从和哨兵模式
http://www.bjpowernode.com/tutorial_springboot/831.html