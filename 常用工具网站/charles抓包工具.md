<!--
 * @Author: your name
 * @Date: 2022-01-25 12:35:05
 * @LastEditTime: 2022-01-25 14:37:06
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /zhiyuanyun/Users/wuqiang/workspace/blog/常用工具网站/charles抓包工具.md
-->
# charles抓包工具
***

## charles下载安装，免费激活
https://www.cnblogs.com/zwj145/p/12995535.html
https://www.zzzmode.com/mytools/charles/ (随便输入一个名字，然后生成破解码，打开charles里面的help填写名字和破解码即可)
https://www.jianshu.com/p/3b3574c22e70

## 如何安装证书，解决https乱码
https://www.cnblogs.com/misection/p/15599570.html
点击help => ssl proxy => install charles root certificate
如果显示证书不被信任，则点击钥匙串访问里头的登录，点击不被信任的charles证书，点开”信任“，改系统默认为总是信任即可
再打开proxy => ssl proxy setting => port改为443，host 默认为 *即可
https://www.cnblogs.com/xuehaoyue/p/14327929.html

手机上设置好代理之后，还需要安装证书，
https://blog.csdn.net/qq_39720249/article/details/121330781
设置 => 安全设置 => 更多安全设置 => 加密与凭据 => 从存储设备安装 => 点击左上角的更多，展开选择下载内容里头的文件即可

## 微信小程序在高版本安卓上无法抓包的原因（安卓微信更新到7.0后，用fidder无法抓包小程序https，大家有什么解决方案）
`最近在开发调试微信小程序，开发完成后用自己的安卓手机查看体验版时，打开fiddler抓包代理工具，发现小程序获取列表失败并报request:fail-202:net:ERR_CERT_AUTHORITY_INVALID 错误，可是关闭fiddler后有能正常浏览。`
```js
1、安卓系统7.0以下版本，不管微信任意版本，都会信任系统提供的证书
2、安卓系统7.0以上版本，微信7.0以下版本，微信会信任系统提供的证书
3、安卓系统7.0以上版本，微信7.0以上版本，微信只信任它自己配置的证书。
目前安卓手机唯一可行的方案是降级微信版本到7.0以下就可以正常抓包了。
```
`谷歌后发现在Android7.0及以上的系统中，每个应用可以定义自己的可信CA集。默认情况下，应用只会信任系统预装的CA证书，而不会信任用户安装的CA证书。这里微信7.0及以上版本只信任自己内置的证书`

https://www.cnblogs.com/jesse131/p/12441094.html