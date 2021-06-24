# android的几种布局方式
***

## LinearLayout(线性布局)
***
重要属性（必需）`android:orientation`，可选值包括`vertical`和`horizontal`。

* 默认只有在线性布局里`layout_weight`属性才有效。
* 一旦View设置了layout_weight属性，那么该View的宽度（或者高度）等于layout_width(或layout_height)的值加上剩余空间的占比。

## RelativeLayout(相对布局)
***
android:layout_centerHorizontal水平居中
android:layout_centerVertical 垂直居中
android:layout_centerInparent 相对于父元素完全居中
android:layout_alignParentBottom 紧贴父元素的左边沿
android:layout_alignParentTop 紧贴父元素上边沿
android:layout_alignParentLeft 紧贴父元素左边
android:layout_alignParentRight 紧贴父元素右边
android:layout_below 在某元素下方
android:layout_above 在某元素上方
android:layout_toLeftOf 在某元素左边
android:layout_toRightOf 在某元素右边
android:layout_alignTop 本元素的上边与目标元素上边对齐
android:layout_alignLeft 本元素左边与目标元素左边对齐
android:layout_alignRight 本元素右边与目标元素右边对齐
android:layout_alignBottom 本元素下边与目标元素下边对齐

其中，在API16版本以上，Left可以改成start, right可以改成end，效果一样的，这是因为有的国家文字是从右到左的，使用start和end可以解决这种本地化 的问题。

## FrameLayout (帧布局)
***
在FrameLayout内部，写在后面的控件默认都会显示在之前的控件上面，android5.0（对应的版本号是21）以后，如果有按钮控件，按钮无论写在前面还是后面，默认都显示在最前面，因为按钮就是用来与用户直接交互的控件，不允许遮挡。

## GridLayout(网格布局)
***
网格布局，是android4.0之后的API才提供的，算是一个相对新的布局容器，他的用法也很简单，类似LinearLayout可以指定方向，也可以指定控件占用多少行列的空间。
GridLayout完全可以取代TableLayout。

```java
<GridLayout android:columnCount="4" android:orientation="horizontal" android:rowCount="5" />

## CoordinatorLayout
***
在谷歌开发者大会上，谷歌引入了Android Design Support Library(后面简称ADSL)来帮助码农在APP中使用Material Design。

```
dependencies {
  compile 'com.android.support:design:25.1.0'
}
```