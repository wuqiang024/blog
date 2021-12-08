# Toolbar, AppBarLayout
***
如果需要设置自己的ActionBar，需要
1、在style文件里将parent改成`Theme.MaterialComponents.Light.NoActionBar`
2、在布局文件中引入
```java
<androidx.appcompat.widget.Toolbar />
3、在activity中设置`setSupportActionBar(toolbar)`
4、在activity中
```java
override fun onOptionsCreated(menu:MenuItem):Boolean {
  menuInflater.inflate(R.menu.toolbar_menu, menu)
  return true
}
```
5、在布局文件中，如果要滚动的话，将toolbar包裹在AppBarLayout里头
```java
<com.google.android.material.appbar.AppBarLayout>
```
6、在recyclerview里头加上`app:layout_behavior="@string/appbar_scrolling_view_behavior`
