# BottomNavigationView
`https://blog.csdn.net/BigBoySunshine/article/details/105774561`
***
## 基本用法
***
1、添加依赖:
`implementation 'com.google.android.material:material:1.0.0'

2、布局中引入
```xml
<com.google.android.material.bottomnavigation:BottomNavigationView
  android:id="@+id/nav_view"
  android:layout_width="0dp"
  android:layout_height="wrap_content"
  android:layout_marginStart="0dp"
  android:layout_marginEnd="0dp"
  android:background="?android:attr/windowBackground"
  app:menu="@menu/bottom_nav_menu"
/>
```

3、常用属性:
* app:itemTextColor 文字的颜色，可以通过selector来控制选中和未选中的颜色
* app:itemIconTint 图标的颜色，可以通过selector来控制选中和未选中的颜色
* app:itemIconSize 图标大小 默认24dp
* app:itemBackground 背景颜色 默认是主题的颜色
* app:itemRippleColor 点击后的水波纹颜色
* app:itemTextAppearanceActive 设置选中时的文字样式
* app:itemTextAppearanceInactive 设置默认的文字样式
* app:itemHorizontalTranslationEnabled 在label visibility 模式为selected时item水平方向移动
* app:elevation 控制控件顶部的阴影
* app:labelVisibilityMode 文字的显示模式
* app:menu 指定菜单xml文件（文字和图片都写在这里面)

4、menu文件:
```xml
<menu xmlns:android="http://schemas.android.com/apk/res/android">
  <item android:id="@+id/navigation_item1" android:icon="@drawable/ic_home_black_24dp" android:title="@string/title_size" />
  <item android:id="@+id/navigation_item1" android:icon="@drawable/ic_home_black_24dp" android:title="@string/title_size" />
  <item android:id="@+id/navigation_item1" android:icon="@drawable/ic_home_black_24dp" android:title="@string/title_size" />
</menu>
```

在每个item中设置对应的icon和title即可。这里的icon可以是一个drawable，也可以是包含不同状态对应不同图片的selector。设置了menu之后一个基本的底部菜单栏就有了。

5、常用事件
主要有两个事件`OnNavigationItemSelectedListener`和`OnNavigationItemReselectedListener`
```java
  nav_view.setOnNavigationItemSelectedListener {
    BottomNavigationView.OnNavigationItemSelectedListener {
      when(it.itemId) {
        R.id.navigation_item1 -> {
          ...
          return @OnNavigationItemSelectedListener true
        }
      }
      false
    }
  }
```

```java
nav_view.setOnNavigationItemReselectedListener(
  BottomNavigationView.OnNavigationItemReselectedListener {
    ...
  }
)
```

两个事件的用法是一样的，区别在于：`OnNavigationItemSelectedListener`在item由未选中到选中状态时触发，而`OnNavigationItemReselectedListener`在item处于选中状态再次点击时触发。

6、最大item数量
`BottomNavigationView`对显示的item数量做了限制，最多5个，超出就会抛出异常。

## 配合fragment
***
单纯使用`BottomNavigationView`并没有什么用，一般都是配合fragment来使用。配合fragment使用时有三种方式:
1、FrameLayout + FragmentTransaction
比较古老的一种方式是通过`getSupportFragmentManager().beginTransaction()`获取到`FragmentTransaction`，然后通过`FragmentTransaction`的`add`,`show`,`hide`等方法来控制fragment的显示。

2、ViewPager
`ViewPager`一种比较流行的方式，当然你也可以用`ViewPager2`，用法差不多，需要在布局文件中添加`ViewPager`
参考`https://blog.csdn.net/BigBoySunshine/article/details/105774561`

3、配合navigation
这种方式是googl官方目前主推的方式。

布局文件如下:
```xml
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:app="http://schemas.android.com/apk/res-auto"
  android:id="@+id/container"
  android:layout_width="match_parent"
  android:layout_height="match_parent"
>
  <com.google.android.material.bottomnavigation.BottomNavigationView
    android:id="@+id/nav_view"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:layout_marginHorizontal="0dp"
    android:background="?android:attr/windowBackground"
    app:layout_constraintBottom_toBottomOf="parent"
    app:menu="@menu/bottom_nav_menu"
  />

  <fragment
    android:id="@+id/nav_host_fragment"
    android:name="androidx.navigation.fragment.NavHostFragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    app:defaultNavHost="true"
    app:layout_conatraintBottom_toTopOf="@id/nav_view"
    app:navGraph="@navigation/mobile_navigation" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

2、navigation文件
```xml
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:app="http://schemas.android.com/apk/res-auto"
  xmlns:tools="http://schemas.android.com/tools"
  android:id="@+id/mobile_navigation"
  app:startDestination="@+id/navigation_home">
  <fragment android:id="@+id/navigation_item1"
    android:name="per.wsj.bottommenu.ui.fragment.Fragment1"
    android:label="@string/title_home"
    tools:layout="@layout/fragment_home" />
</navigation>
```
在navigation中指定来对应的fragment

3、Activity中
接下来的使用就很简单了，调用Activity的扩展函数`findNavController`,根据布局文件中的`fragment`标签的id获取`NavController`,将`NavController`和`BottomNavigationView`绑定即可，如下:
```java
val navView: BottomNavigationView = findViewById(R.id.nav_view)
val navController = findNavController(R.id.nav_host_fragment)
navView.setupWithNavController(navController)
```

## 显示badge(角标/悬浮徽章)
***
1、基本使用
在BottomNavigationView上添加badge很简单，提供了如下操作badge的方法:
* getBadge(int menuItemId) 获取badge
* getOrCreateBadge(int menuItemId) 获取或创建badge
* removeBadge(int menuItemId) 移除badge

因此添加一个badge只需要如下代码：

```java
val navView: BottomNavigationView = findViewById(R.id.nav_view)
val badge = navView.getOrCreate(R.id.navigation_dashboard)
badge.number = 20
```

2、常用属性
`getBadge`和`getOrCreateBadge`返回的都是`BadgeDrawable`,`BadgeDrawable`常用属性如下:
* backgroundColor 设置背景色
* badgeGravity 设置角标的位置，有四种可选:`TOP_START`,`TOP_END`,`BOTTOM_START`,`BOTTOM_END`，分别对应左上角，右上角，左下角，右下角。
* badgeTextColor 设置文字颜色
* maxCharacterCount 最多显示几位数字，比如该项设置了3，number设置为108，则显示99+

3、注意事项
需要你的Application的Theme继承自`Theme.MaterialComponents`

4、扩展
同样是位于com.google.android.material包中的TabLayout也可以用同样的方式添加badge
```java
tabLayout.getTabAt(0).getOrCreateBadge.apply {
  number = 10
  backgroundColor = Color.RED
}
```

## 常用需求
1、动态显示/隐藏MenuItem