# ImageView的scaleType属性
***
scaleType是缩放的方式，默认就是“fitCenter"，表示图片会填充控件，不会让图片变形。

`android:scaleType="fitXY"`
表示图片填充控件，但是允许图片被拉伸变形

`android:scaleType="fitCenter"`
表示图片填充控件，但是不允许变形，类似于contain

`android:scaleType="centerCrop"`
以填满控件为目的，将原图的中心对准ImageView中心，等比例放大原图，知道填满ImageView为止(ImageView的宽和高都要填满),原图超过ImageView的部分做裁剪处理。

`android:scaleType="center"`
保持原图的大小，显示在ImageView的中心，当原图的size大于ImageView的size时，对超出部分进行裁剪

`android:scaleType="matrix"`
不改变原图的大小，从ImageView的左上角开始绘制图，原图超过ImageView的部分做裁剪处理。

`android:scaleType="fitEnd"`
把原图按比例放大（缩小到）与ImageView的高度，显示在ImageView的下部分位置

`android:scaleType="fitStart"`
把原图按比例扩大（缩小）到ImageView的高度，显示在ImageView的上部分位置

`android:scaleType="centerInside"`
以原图完全显示为目的，将图片的内容完整居中显示，通过按比例缩小原图的size等于或小于ImageView的高宽，如果原图的size本身就小于ImageView的size，则原图的size不做任何处理，居中显示在ImageView。

