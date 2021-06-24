# Service
***
`Service Intent must be explicit: Intent 解决`
在Activity中启动Service服务的时候报错，服务意图必须是显性声明。 这是为了防止造成冲突（i.e. 有多个Service用同样的intent-filter的情况)。
这是Android 5.0 (Lollipop) 之后的规定。 不能用包名的方式定义Service Intent, 而要用显性声明:   new Intent(context, xxxService.class);

```java
Intent intent = new Intent(this, com.yulore.test.AppService.class);  
context.startService(intent);  
```

如果想继续用隐式意图的话，加上包名信息即可。
```java
Intent intent = new Intent();  
intent.setAction("com.yulore.recognize.android");  
intent.setPackage(context.getPackageName());    //兼容Android 5.0  
context.startService(intent); 
```