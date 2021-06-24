# Material Design
***
google从android5.0开始，将所有内置的应用都使用Material Design风格进行设计。

## Toolbar
***
在`res/values/styles.xml`中，有如下代码:
```xml
<style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
</style>
```
这里定义了一个名叫AppTheme的主题，然后指定它的parent主题是`Theme.AppCompat.Light.DarkActionBar`，这个`DarkActionBar`就是一个深色的ActionBar主题，我们之前所有项目中自带的ActionBar就是因为指定了这个主题才出现的。

而现在我们准备使用Toolbar来替代ActionBar，因此需要指定一个不带ActionBar的主题，通常有`Theme.AppCompat.NoActionBar`和`Theme.AppCompat.Light.NoActionBar`两种主题可选。

其中`Theme.AppCompat.NoActionBar`表示深色主题，它会将界面颜色设为深色，陪衬颜色设为浅色。我们一般使用浅色主题。

```xml
<androidx.appcompat.widget.Toolbar
  android:theme="@style/ThemeOverlay.AppCompat.Dark.ActionBar"
  app:popupTheme="@style/ThemeOverlay.AppCompat.Light"
  android:layout_height="?attr/actionBarSize"  // 这里代表使用默认的actionBar的高度
>
```
在activity文件中要这样设置
```java
setSupportActionBar(toolbar)
```

## ThemeOverlay.AppCompat
***
作为Application Theme的parent主题, Theme.AppCompat提供了诸多属性设置App全局Theme样式，但是有时候，我们还需要单独给某个或某些view设置不同的样式，这种情况下,ThemeOverlay.AppCompat就派上用场了。
正如命名所表达的含义一般，ThemeOverlay.AppCompat 系列主题用于覆盖基本的 AppCompat.Theme 样式，按照需求仅仅改变部分属性的样式。这里列举一些常见用法：

ThemeOverlay.AppCompat

继承自 @style/Base.ThemeOverlay.AppCompat。这是一个空主题，但是却将 AppCompat 主题中的相关属性复制了一遍。这在给个别 View 单独设置部分样式时非常实用。

```xml
<style name="AppTheme.Secondary" parent="ThemeOverlay.AppCompat">
    <item name="colorAccent">@color/colorPrimary</item>
</style>
```
然后再借助`android:theme`将其绑定到元素上。`android:theme="AppTheme.Secondary"`,在这个例子中，重写了`colorAccent`属性，同时保证其他属性沿用parent 为 Theme.AppCompat 的 AppTheme 中的设置。从 ThemeOverlay.AppCompat 文档介绍中可以看出，比如 colorPrimary 属性是这样复制的：
`android:colorPrimary = ?attr/colorPrimary`

参考文献: https://blog.csdn.net/xdy1120/article/details/102503956

## 新建menu文件
***
在res下 New -> Menu Resource file, 创建一个toolbar.xml文件。
```xml
<menu>
  <item android:id="@+id/menu1" android:title="backup" app:showAsAction="always"></item>
</menu>
```
我们通过item来设置action按钮，`android:id`指定id,`android:icon`指定用于按钮的图标，`android:title`指定按钮的图片。
接着使用`app:showAsAction`来指定按钮的显示位置，这里再次使用来app的命名空间，同样是为了兼容低版本的系统。主要有以下几种值可选。

`always`表示永远显示在toolbar中，如果屏幕空间不够则不显示
`ifRoom`表示屏幕空间足够的情况下显示在toolbar中，不够的话就显示在菜单中
`never`则表示永远显示在菜单中
`注意:` toolbar中的action只会显示图标，menu中的action只会显示文字

在activity中代码
```java
override fun onCreateOptionsMenu(menu: Menu): Boolean {
  menuInflater.inflate(R.menu.toolbar, menu)
  return true
}

override fun onOptionsItemSelected(item: MenuItem): Boolean {
  when(item.itemId) {
    R.id.backup -> {}
    R.id.settings -> {}
    else -> {}
  }
  return true
}
```

非常简单，我们在onCreateOptionsMenu中加载了toolbar.xml这个菜单文件，然后在onOptionsItemSelected方法中处理各个按钮的点击事件。

## DrawerLayout
***
它是一个布局，在布局中允许放入两个直接子控件，第一个子控件是主屏幕中的内容，第二个子控件是滑动菜单中显示的内容。
```xml
<DrawerLayout>
  <FrameLayout android:layout_width="match_parent" android:layout_height="match_parent">
    <Toolbar></Toolbar>

  </FrameLayout>
  <TextView android:layout_width="match_parent" android:layout_height="match_parent"/>
</DrawerLayout>
```

```java
suportActionBar?.let {
  it.setDisplayHomeAsUpEnabled(true)
  it.setHomeAsUpIndicator(R.drawable.ic_menu)
}

override fun onOptionsItemSelected(item: MenuItem): Boolean {
  when(item.itemId) {
    android.R.id.home -> drawlayout.openDrawer(GravityCompat.START)
  }
}