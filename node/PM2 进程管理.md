## 为什么需要进程管理器
***
做过服务端开发的朋友应该比较清楚，在生产环境运行一个web服务,并不是只是简单的把服务启动起来就可以。
为了确保服务质量，至少需要完成下面事情：

* 服务器异常重启
* 服务资源占用情况监控
* 配置灵活更改（加自动重启生效）
* 集群部署(性能相关)

这个时候，进程管理器显得非常重要。目前常用的node进程管理器有PM2,forever等。

## PM2安装
方便起见，一般都采取全局安装。
`npm install -g pm2`


## 启动服务

`pm2 start -w ./bin/www`

-w 表示，当项目文件发生变化时，服务自动重启。


## 其他PM2命令
```bash
pm2 save # 保存当前运行的设置
pm2 start app.js -i 4  // 后台运行Pm2 ,启动4个app.js
pm2 list // 显示所有进程
pm2 monit // 监视所有进程
pm2 logs // 显示所有进程日志
pm2 stop all  // 停止所有进程
pm2 stop 0  // 停止指定进程
pm2 restart 0 // 重启指定进程
pm2 restart all // 重启所有进程
pm2 delete 0  // 杀死指定进程
pm2 delete all  // 杀死所有进程
pm2 web  // 运行健壮的computer api endpoint
pm2 startup  // 产生init脚本，保持进程或者
```

## 运行进程的不同方式
``` bash
pm2 start app.js -i max // 跟进cup数量启动最大进程数目
pm2 start app.js -i 3  // 启动3个进程
pm2 start app.js -x // 用fork模式启动，而不是使用cluster
pm2 stop serverone  // 停止名为serverone的进程
pm2 start app.js -x -- -a 23  // 用fork模式启动app.js并传递参数(-a 23)
pm2 start app.json  // 启动进程，在app.json里设置选项
pm2 start app.js -i max -- -a 23  // 在--之后给app.js并传递参数
pm2 start app.js -i max -e err.log -o out.log  // 启动并生成一个配置文件
```


## 查看当前运行的服务
```bash
pm2 list
```

## 重启服务
有的时候，服务运行久了，资源占用比较厉害，可以重启服务。

```bash
pm2 restart ./bin/www
pm2 restart www
pm2 restart 0
```

## 使用配置文件
***
如果都在命令行完成，不但繁琐，还容易出错。这个时候就可以通过配置文件来完成。

```bash
{
	"name": "fis-receiver",  // 应用名称
	"script": "./bin/www",  // 实际启动脚本
	"cwd": "./",  // 当前工作路径
	"watch": [  // 监控变化的目录，一旦变化，自动重启
		"bin",
		"routes"
	],
	"ignore_watch": [  // 从监控目录中排除
		"node_modules",
		"logs",
		"public"
	],
	"watch_options": {
		"followSymlinks": false
	},
	"error_file": "./logs/app-err.log",  // 错误日志路径
	"out_file": "./logs/app-out.log",  // 普通日志路径
	"env": {
		"NODE_ENV": "production"  // 环境参数，当前指定为生产环境
	}
}
```

这个时候，可以这样启动服务。
`pm2 start app.json`


## 你也可以执行用其他语言编写的app
```bash
pm2 start my-bash-script.sh -x 
pm2 start my-python-script.py -x
```