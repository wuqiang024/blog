# Intent
***
Intent(意图)是四大组件的枢纽，安卓通信的桥梁。

`startActivity(Intent)/startActivityForResult(Intent)`来启动Activity

`startService(Intent)/bindService(Intent)`来启动Service

`sendBroadcast` 来发送广播到指定BroadcastReceiver

## 隐式Intent和显式Intent的区别
***
*显示Intent:* 通过组件名指定启动的组件.`startActivity(new Intent(A.this, B.class))；每次启动的组件只有一个。

*隐式Intent:* 不指定组件名，而指定Intent的Action, Data或Category,当我们启动组件时，会去匹配AndroidManifest.xml相关组件的Intent-filter，逐一匹配出满足属性的组件，当不止满足一个组件时，会弹出一个让我们选择启动哪个的对话框。

## Intent的七个属性
***
1、ComponentName(组件名称)
就是目标组件的名称，由组件所在应用程序配置文件中的包名+组件的全限定类名组成，这是一个显式的Intent，激发的组件只有一个！
可以通过`setClass`,`setClassName`或`setComponent`方法设置，使用`getComponent`方法获取。

```java
ComponentName cn = new ComponentName(A.this, B.class);
Intent it = new Intent();
it.setComponent(cn);
```

其实，上面的代码直接写成`Intent it = new Intent(A.this, B.class)即可。
在跳转到的Activity页面，调用`getIntent().getComponent()`方法获取对象，然后通过`getPackageName()`获取包名，通过`getClassName()`获取类名。

2、Action(动作)
一个普通的字符串，代表Intent要完成的一个抽象动作，但是具体由哪个组件来完成，Intent并不负责，就是仅仅知道会有这个动作，谁来完成就交给Intent-filter来筛选。
要注意在java中的Action和Intent-filter中的格式是不一样的。
```java
<action android:name="android.intent.action.CALL"/>
intent.setAction(Intent.CALL_ACTION)
```

3、Category(类别)
同样是普通的字符串，Category则用于为Action提供额外的附加类别信息，两者通常结合使用，一个Intent对象只能有一个Action，但是能有多个Category。
```java
<category android:name="android.intent.category.DEFAULT"/>
intent.addCategory(Intent.CATEGORY_DEFAULT)
```

4、Data(数据), Type(MIME类型)
Data通常用于向Action属性提供操作的数据，接受一个URI对象，URI的格式:`scheme://host:port/path`。
参数依次为：协议头，主机，端口，路径。
Type通常用于指定Data所制定的Uri对应的MIME类型，比如能够显示数据的组件不应该用来播放音频文件，可以是自定义的MIME类型，只要符合`abc/xyz`格式的字符串就可以了。

如果我们在java中进行设置，这两个属性是会相互覆盖的，如果需要两个属性都有的话，就要调用setDataAndType()方法进行设置。而在AndroidManifest.xml文件中，这两个属性都是存放在data标签中的。
```xml
<data
  android:mimeType=""
  android:scheme=""
  android:host=""
  android:port=""
  android:path=""
  android:pathPrefix=""
  android:pathPattern=""
/>
```

5、Extras(额外)
通常用于多个Action之间的数据交换，Extras属性是一个Bundle对象，通过键值对进行数据的存储
单个变量：
intent.putIntExtra(), intent.getIntExtra()
多个变量：
intent.putExtras(Bundle), intent.getExtras();

6、Flags(标记)
表示不同来源的标记，多数用于只是Android如何启动Activity以及启动后如何对待，标记都定义在Intent类中.

## 显式使用Intent的示例
1、返回Home界面
```java
Intent intent = new Intent();
intent.setAction(Intent.ACTION_MAIN);
intent.addCategory(Intent.CATEGORY_HOME);
startActivity(intent);
```

2、打开百度网页
```java
Intent it = new Intent();
it.setAction(Intent.ACTION_VIEW);
it.setData(Uri.parse("http://www.baidu.com"));
startActivity(it);
```

3、打开摄像头拍照
```java
Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
startActivityForResult(intent, 0);

Bundle extras = intent.getExtras();
Bitmap bitmap = (Bitmap) extras.get("data");
```

4、进入手机设置页面（无线网络设置)
```java
Intent intent = new Intent(android.provider.Settings.ACTION_WIRELESS_SETTINGS);
startActivityForResult(intent, 0);
```