# drawable的渐变
***

```xml
<shape xmlns:android="http://schemas.android.com/apk/res/android">
  <gradient android:angle="integer"
  android:centerX="integer"
  android:centerY="integer"
  android:centerColor="integer"
  android:startColor="color"
  android:endColor="color"
  android:gradientRadius="integer"
  android:type=["linear" | "radial" | "sweep"]
  android:useLevel=["true" | "false"] />
</shape>
```

`android:angle`代表角度，0是从left到right, 90是从bottom到top，180是从right到left, 270是从top到bottom。角度数值必须是45到整数倍。
默认是0，该属性只有在type=linear到情况下起作用，默认到type为linear。

`android:startColor` 颜色渐变开始颜色

`android:endColor` 颜色渐变结束颜色

`android:centerColor` 颜色渐变中间颜色，主要用于多彩

`android:centerX` (0 - 1.0) 相对于X轴的渐变位置

`android:centerY` (0 - 1.0) 相对于Y轴的渐变位置

以上两个属性只有在type不为linear情况下起作用

`android:gradientRadius` 渐变颜色的半径，单位应该是像素点，需要`android:type="radial"`，如果`android:type="radial"`没有设置`android:gradientRadius`将会报错。

