<!--
 * @Author: wuqiang
 * @Date: 2022-06-16 02:47:39
 * @LastEditors: wuqiang
 * @LastEditTime: 2022-06-16 02:52:38
-->
# npm 源
***
npm安装包是从国外服务器上下载的，受网络因素影响比较大，可能会出现异常。因此，国内的淘宝团队同步npm实现了npm的国内源。我们可以在使用npm安装包时配置淘宝的国内源，命令如下:

```sh
npm --registry=hppts://registry.npm.taobao.org
```

为了方便使用，淘宝团队不仅提供了上述镜像，还开发了一个更易用的工具CNPM(https://npm.taobao.org)，命令如下:

```
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

## nrm
***
如果想使用其他非淘宝的镜像源，还可以安装一款名为nrm的镜像源管理工具，命令如下:

```
npm install -g nrm
```

然后查看所有可用的镜像:

```
nrm ls
nrm use taobao
```