# Android编译时提示“Namespace ‘app’ not bound”
***

主要的问题是根节点少了一个声明。
补上

```
xmlns:app="http://schemas.android.com/apk/res-auto"
```