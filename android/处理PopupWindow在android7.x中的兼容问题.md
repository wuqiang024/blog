# 处理PopupWindow在android7.x中的兼容问题
***
`问题描述:PopupWindow中的showAsDropDown(View anchor)用于在指定锚点View下方显示PopupWindow,在android7.0(api <= 23)之前是没什么问题的，但是在android7.x上会在某些情况下出现兼容情况:

1、如果指定PopupWindow的高度为MATCH_PARENT，调用showAsDropDown(View anchor)时，在7.0之前，会在锚点anchor下边缘到屏幕底部之间显示PopupWindow；而在7.0, 7.1系统上的PopupWindow会占据整个屏幕(除状态栏外)

2、如果指定PopupWindow的高度为WRAP_CONTENT，调用showAsDropDown(View anchor)时，便不会出现兼容性问题

3、如果指定PopupWindow的高度为自定义的值height，调用showAsDropDown(View anchor)时，如果height > 锚点下边缘到屏幕底部的距离，则还是会出现7.0, 7.1上显示的异常，否则，不会出现该问题。可以看出，情况1和2是情况3的特例。

## 解决方案
***
如果出现上述分析中的兼容问题，可以使用showAtLocation()方法替代showAsDropDown()，详情可参考(https://link.jianshu.com/?t=https://github.com/tianma8023/PopupWindowCompat/blob/master/app/src/main/java/com/tianma/popupwindowsample/MainActivity.java)

```java
if (Build.VERSION.SDK_INT >= 24) { // Android 7.x中,PopupWindow高度为match_parent时,会出现兼容性问题,需要处理兼容性
    int[] location = new int[2]; // 记录anchor在屏幕中的位置
    anchor.getLocationOnScreen(location);
    int offsetY = location[1] + anchor.getHeight();
    if (Build.VERSION.SDK_INT == 25) { // Android 7.1中，PopupWindow高度为 match_parent 时，会占据整个屏幕
        // 故而需要在 Android 7.1上再做特殊处理
        int screenHeight = ScreenUtils.getScreenHeight(context); // 获取屏幕高度
        popupWindow.setHeight(screenHeight - offsetY); // 重新设置 PopupWindow 的高度
    }
    popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, 0, offsetY);
} else {
    popupWindow.showAsDropDown(anchor);
}
```