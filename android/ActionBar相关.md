# ActionBar相关
***
```java
ActionBar supportActionBar = getSupportActionBar();
supportActionBar.setTitle("我是actionbar title");
supportActionBar.setSubTitle("good");

@Override
public boolean onCreateOptionsMenu(Menu menu) {
  getMenuInflater().inflate(R.menu.menu_app_bar, menu);
  return ture;
}
```

同时需要在res文件夹下新建menu文件夹，创建`menu_app_bar.xml`文件。

```xml
<menu ...>
  <item
    android:id="@+id/action_setting"
    android:icon="@mipmap/ic_launcher"
    android:showAsAction="always" />
</menu>
```
下面介绍几个重点属性:
android:title 为菜单标题
android:icon 为菜单标题
android:orderInCategory 表示显示的优先级
app:showAsAction 表示显示的方式，其中，nerver表示从不显示到外面，always一直显示到ActionBar上面，ifRoom表示如果ActionBar空间足够就显示到上面，空间不够隐藏到overflow里面。

用`onOptionsItemSelected`处理菜单的点击事件，在Activity中重写方法。

```java
@Override
public boolean onOptionsItemSelected(MenuItem item) {
  int id = item.getItemId();

  if(id == R.id.action_settings) {

  }
}
```

## 设置ToolBar代替ActionBar
***
```java
Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
setSupportActionBar(toolbar);
toolbar.setNavigationIcon(R.mipmap.back);
toolbar.setNavigationOnClickListener(new View.OnClickListener() {
  @Override
  public void onClick(View v) {
    // 处理事件
  }
})
toolbar.setLogo(R.mipmap.ic_launcher);
```