# WebView相关问题
***

## A: WebView无法加载网页
***
Q: Android SDK升级造成的，从Android 9(API级别28), 默认情况下限制了明文流量的网络请求，对未加密流量不再信任，直接放弃请求，因此http的url均无法在webview中加载，`https 不受影响`。

***`解决方案`一***

```
<manifest ...>
    <application
        ...
        android:usesCleartextTraffic="true"
        ...>
        ...
    </application>
</manifest>
```

***`解决方案二`***
res 下新建 xml 目录，创建文件：network_security_config.xml ，内容如下

```
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

在 AndroidManifest.xml 的 application 标签添加配置：

```
<manifest ...>
    <application
        ...
        android:networkSecurityConfig="@xml/network_security_config"
        ...>
        ...
    </application>
</manifest>
```

***`解决方案三` 【推荐】***
服务器和本地应用都改用 https

***`解决办法四`***
targetSdkVersion 降级回到 27

## 即便是https协议也无法打开html页面
***
这个只有在android端才会出现，在ios没有这个现象
首先，要在`AndroidManifext.xml`文件下加上网络访问权限` <uses-permission android:name="android.permission.INTERNET"/>`
然后在activity文件里使用如下代码
```js
webview.settings.javaScriptEnabled = true  // 这个很关键，有的spa页面因为是js执行的，如果不加上就不会展示页面
webview.webViewClient = WebViewClient()
webview.loadUrl("https://www.niuerduo.com")
```