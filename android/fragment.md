# Fragment
***
一般来说只需要实现以下生命周期方法。

* onCreate()
系统会在创建片段时调用此方法。应该在实现内初始化想在片段暂停或停止后恢复时保留的必需片段组件。

* onCreateView()
系统会在片段首次绘制其用户界面时调用此方法。要想为片段绘制UI,从此方法中返回的View必须是片段布局的根视图。如果片段未提供UI，可以返回null。

* onPause()
系统将此方法作为用户离开片段的第一个信号（但并不总是意味着此片段会销毁）进行调用。通常应该在此方法内确认在当前用户会话结束后仍然有效但任何更改（因为用户可能不返回）。

## 创建Fragment
***
创建Fragment一般分为三步走：
1、为Fragement定义一个布局
2、定义类继承Fragment
3、重写类中的onCreateView方法，返回一个View对象作为当前Fragment的布局。Fragment第一次绘制它的用户界面的时候，系统会调用onCreateView()方法。为了绘制fragment的UI，此方法必须返回一个作为Fragment布局的根的Vie为。如果Fragment不提供UI,可以返回null。

```
import android.app.Fragment

public class LeftFragment extends Fragment {
  @Override
  public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    View view = inflater.inflate(R.id.fragment_left, container, false);
  }
}

## 添加替换Fragment
```
ExampleFragment fragment = new ExampleFragment();
FragmentManager manager = getFragmentManager();
FragmentTransaction transaction = manager.beginTransaction();
transaction.add(R.id.fragment_container, fragment);
transaction.commit();
```

然后可以用add(), replace(), remove()等方法进行操作。