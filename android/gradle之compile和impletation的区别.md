# gradle之compile与impletation的区别
***
2017年后，google将android studio版本更新至3.0，更新中，连带着com.android.tools.build:gradle工具也升级到了3.0.0，在3.0.0中使用了最新的gradle 4.0里程碑版本作为gradle的编译版本，该版本gradle编译速度有所加速，更加欣喜的是，完全支持java8。
当然，对于kotlin的支持，在这个版本也有所体现，kotlin插件是默认安装的。

在com.android.tools.build:gradle 3.0以下版本，依赖在gradle中的声明写法
```
compile fileTree(dir: 'libs', include: ['*.jar'])
```

但在3.0后的写法为
```
implementation fileTree(dir: 'libs', include: ['*.jar'])
或者
api fileTree(dir: 'libs', include: ['*.jar'])
```

api指令完全等同于compile指令，你将所有的compile改为api，完全没有错。

`implementation指令`
```
使用了该命令编译的依赖，它仅仅对当前的Module提供接口。
优点：1、加快编译速度。2、隐藏对外不必要的接口。
```

`provided(compileOnly)`
```
只在编译时有效，不会参与打包
可以在自己的module中使用该方式依赖一些比如com.android.support,gson这些使用者常用的库，避免冲突。
```

`apk(runtimeOnly)`
```
只在生成apk的时候参与打包，编译时不会参与，很少用.
```

`testCompile(testImplementation)`
```
testCompile只在debug模式的编译和最终的debug apk打包时有效
```

`releaseCompile(releaseImplementatioin)`
```
Release compile 仅仅针对release模式的编译和最终的release apk打包
```