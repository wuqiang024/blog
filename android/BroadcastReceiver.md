# BroadcastReceiver
***
BroadcastReceive其实是应用程序间的大喇叭，即通信的一个手段，系统自己在很多时候都会发送广播，比如电量低或者充足，刚启动完，插入耳机，输入法改变等发生的时候，系统都会发送广播，这叫系统广播，每个APP都会收到，如果你想让你的应用在接收到这个广播的时候做一些操作，那么只需要注册一个用于监视开机的BroadcastReceiver。

## 两种广播类型
1、标准广播
完全异步执行的广播，所有广播接收器几乎会在同一时刻收到这条广播通知

2、有序广播
同步执行的一种广播，发出广播后，同一时间只有一个广播接受者能收到，当这个广播接收者的逻辑执行完后，才会传递到下一个接收者，当然，前面的接受者还可以截断广播的继续传递，那么后续接收者就无法收到广播了。

## 两种注册广播的方式
1、动态注册
就是在java代码中指定IntentFilter，然后添加不同的Action即可，想监听什么什么广播就监听什么广播，另外，动态注册的广播，一定要调用unregisterReceiver来让广播取消注册

2、静态注册
动态注册需程序启动后才能接收广播，静态注册就弥补来这个短板，在AndroidManifest中制定<IntentReceiver>就可以让程序在未来启动的情况下接收到广播来。

```java
// 自定义一个BroadcaseReceiver 在onReceive方法中完成广播要处理的事物
public class MyReceiver extends BroadcastReceiver {
  @Override
  public void onReceive(Context context, Intent intent) {
    // do something
  }
}
```

```java
MyReceiver receiver = new MyReceiver();
IntentFilter filter = new IntentFilter();
filter.addAction("android.net.conn.CONNECTIVITY_CHANGE");
registerReceiver(receiver, filter);

@Override
public void onDestroy() {
  super.onDestroy();
  unregisterReceiver(receiver);
}
```

`动态注册有个缺点就是需要程序启动才可以接收广播，假如要程序还未启动就可以接收广播的话，就需要注册静态广播`

## 静态注册实例
***
```java
public class MyReceiver extends BroadcastReceiver {
  private final String ACTION_BOOT = "android.intent.action.BOOT_COMPLETED";
  @Override
  public void onReceive(Context context, Intent intent) {
    if(ACTION_BOOT.equals(intent.getAction())) {
      // do something
    }
  }
}
```

在AndroidManifest.xml中进行注册与授权。
```xml
<receiver android:name=".MyReceiver">
  <intent-filter>
    <action android:name="android.intent.action.BOOT_COMPLETED"/>
  </intent-filter>
</receiver>

// 权限
<uses-permision android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
```

## 发送广播
***
```java
sendBroadcast(new Intent("com.example.broadcasttest.MyReceiver"))
```

