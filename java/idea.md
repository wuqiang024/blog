<!--
 * @Author: wuqiang
 * @Date: 2022-04-18 13:16:16
 * @LastEditors: wuqiang
 * @LastEditTime: 2022-04-29 16:45:15
-->
# idea免费激活
***
http://vrg123.com/
关注后即可获得激活码

https://mp.weixin.qq.com/s/2cmHr5VWP8s7rktzUXiEfg

# MySql
***

## 在终端输入mysql -u root -p 出现如下问题: “zsh: command not found: mysql”
***

输入"alias mysql=/usr/local/mysql/bin/mysql"，即可解决:
再输入"mysql -u root -p "，输入密码即可:

## idea执行sql脚本
***
1、Preference => Apearances => Show tool window numbers => 右侧的"datasbase" => "+"号 => mysql

## 在springboot的maven项目启动时，报错：Error:(3, 27) java: 程序包lombok.extern.slf4j不存在错误，编译不报错，maven依赖也合适，项目就是无法启动
解决办法: `Preferences => Build, Execution, Deployment => Build Tools => Maven => Runner => 勾选上 'Delegate IDE  build / ...'`

原因: 
Delegate IDE build/run actions to Maven：将 intelliJ idea中项目构建和运行操作交给Maven；
在不勾选的情况下对项目的构建和运行是 intelliJ idea 去做的，就可能导致构建和运行时无法找到maven仓库中的相关jar包，勾选后在对项目进行构建和运行等操作直接交给了maven。
