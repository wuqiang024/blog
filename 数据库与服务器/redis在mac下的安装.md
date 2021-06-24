# 下载
打开官网https://redis.io/
下载最新稳定版本

# 安装
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