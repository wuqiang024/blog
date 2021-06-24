# Activity生命周期
***

## Activity销毁时保存数据
***
当Activity异常退出的时候会调用onSaveInstanceState()保存数据，重新打开的时候会调用onRestoreInstanceState():

```java
@Override
protected void onSaveInstanceState(Bundle outState) {
  super.onSaveInstanceState(outState);
  outState.putString("key", "value");
}

@Override
protected void onRestoreInstanceState(Bundle savedInstanceState) {
  super.onRestoreInstanceState(savedInstanceState);
  String value = savedInstanceState.getString("key");
}

// 其实onRestoreInstanceState方法不用写，当程序异常退出时，有保存的数据，可以在onCreate方法中取出来
@Override
protected void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  if(savedInstanceState != null) {
    String value = savedInstanceState.getString("key");
  }
}