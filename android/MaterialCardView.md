# MaterialCardView
***
MaterialCardView是实现卡片式布局的重要控件,由Material库提供。实际上就是一个FrameLayout，只是额外提供了圆角和阴影等效果，看上去会有立体的感觉。

```java
<com.google.android.material.card.MaterialCardView
  app:cardCornerRadius="4dp"
  app:elevation="5dp"/>
```

因为MaterialCardView没有什么定位方式，所以一般在它内部再加一个容器用来布局。

如果用在recyclerview里头，需要两个卡片之间有间距的话，可以在MaterialCardView外头包一个LinearLayout用来设置padding。