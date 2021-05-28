# Gestures(手势)
***
手势是：连续触碰的行为，比如上下左右滑动屏幕，又或者是画一些不规则的几何图形，安卓对上述两种手势都提供来支持。

1、安卓提供手势检测，并为手势识别提供了相应的监听器
2、安卓运行开发者自行添加手势，并提供了相应的API识别用户手势

## Android中手势交互的执行顺序
***
1、手指触碰屏幕时，出发MotionEvent事件
2、该事件被OnTouchListener监听，可在它的onTouch()方法中获得该MotionEvent对象
3、通过GestureDetector转发MotionEvent对象给OnGestureListener
4、我们可以通过OnGestureListener获得该对象，然后获得相关信息，以及做相关处理

`MotionEvent`这个类用于封装手势，触摸笔，轨迹球等等的动作事件。其内部封装了两个重要的属性X和Y，这两个属性分别用于记录横轴和纵轴的坐标
`GestureDetector`识别各种手势
`OnGestureListener`这是一个手势交互的监听接口，其中提供了多个抽象方法，并根据GestureDetector的手势识别结果调用相对应的方法。

## GestureListener详解
***
GestureListener手势监听器，通过GestureDetector识别手势，提供下述回调方法

`按下(onDown)`:刚刚手指接触到触摸屏的那一刹那，就是触的那一下
`抛掷(onFling)`:手指在屏幕上迅速移动，并松开的动作
`长按(onLongPress)`:手指按在屏幕上持续一段时间，并且没有松开
`滚动(onScroll)`:手指在屏幕上滚动
`按住(onShowPress)`:手指按在屏幕上，它的时间范围在按下起效，在长按之前
`抬起(onSingleTapUp)`:手指离开触摸屏的那一刹那

实现手势检测很简单，步骤如下：
1、创建GestureDetector对象，创建时需实现GestureListener传入
2、将Activity或者特定组件上的TouchEvent事件交给GestureDetector处理即可。

```java
public class MainActivity extends AppCompatActivity {
  private MyGestureListener mListener;
  private GestureDetector mDetector;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    mListener = new MyListener();
    mDetector = new GestureDetector(this, mListener);
  }
  
  @Override
  public boolean onTouchEvent(MotionEvent event) {
    mDetector.onTouchEvent(event);
  }

  private class MyGestureListener implements GestureDetector.OnGestureListener {
    
  }
}
```

## SimpleOnGestureListener
***
相比起OnGestureListener，SimpleOnGestureListener显得更加简单，想重写什么方法就重写什么方法。