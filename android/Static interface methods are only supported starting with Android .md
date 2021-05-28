# 项目运行报错Error: Static interface methods are only supported starting with Android N (--min-api 24)
***
android studio运行项目提示错误:

```
Error: Static interface methods are only supported starting with Android N (--min-api 24)
```

错误原因: 这是因为java8才支持静态接口方法的原因
提示的意思是最小api应用24，实验将最小api版本改为26后，能在Android O的设备上运行。
但是由于App肯定不能只适配8.0以上的设备，所以还得另寻方法
最后发现这些问题都是因为没有指定jdk1.8而产生的。

解决办法: 可以通过在app的build.gradle文件中配置使用java8编译:
在app build:gradle中的android下添加指定jdk版本的代码，如下:

```
android {
  ...
  compileOptions {
    sourceCompatibility JavaVersion.VERSION_1_8
    targetCompatibility JavaVersion.VERSION_1_8
  }
}
```

重新运行项目即可成功。