# Android中点击链接调起app
***
在h5或者短信中，点击链接则调起app完成相关功能逻辑。

## 原理
***
通过使用自定义Scheme方式，修改Scheme为自己的Scheme来实现调起app。

App通过注册intent-filter声明intent，其他应用发送intent时通过系统级广播传递过来，如果与app预先注册的intent-filter匹配，app将接收到该intent，实现调起APP功能。

## 实现
***
自定义Scheme为: test://mytest.com/path?type=test

1、manifest清单文件中添加intent-filter:

```xml
<activity android:name=".TestActivity">
  <intent-filter>
    <action android:name="android.intent.action.VIEW"/>
    <category android:name="android.intent.category.DEFAULT">
    <category android:name="android.intent.category.BROWSABLE">
    <data android:host="mytest.com"
      android:pathPrefix="/path"
      android:scheme="test" />
  </intent-filter>
</activity>
```

2、在TestActivity.java的onNewIntent()或onCreate()方法中可以接收到相应的参数

```java
  public void handleUri(Intent intent) {
    String action = intent.getAction();
    Uri uri = intent.getData();
    if(uri != null) {
      String type = uri.getQueryParameter("type");
    }
  }
  ```

  ## 其中相关API
  ***
  `getScheme()`: 获取Uri中的scheme部分 => test
  `getHost()`: 获取Uri中的Host部分 => mytest.com
  `getPath()`: 获取Uri中的path部分 => /path
  `getQuery()`: 获取query部分 => type=test
  `getQueryParameter(String key)`: 获取query中key的值 => getQueryParameter("type") 为test

  ## 注意:
  ***
  1、在上述中的handleUri(Intent intent)方法中的intent对象
  (1)对于onCreate()方法通过this.getIntent()获取
  (2)对于onNewIntent()方法则直接使用onNewIntent(Intent intent)中的intent。
  在onNewIntent()方法中如果使用getIntent()获取对象会造成程序已经启动，点击链接地址调起App所获得的uri为Null。

  2、关于getQueryParameter(String key)方法，如果key中值带有"+"，使用此方法获得的值中会自动将"+"替换为空格，导致解密出现问题。
  查阅相关资料，发现这是google api的bug。
  