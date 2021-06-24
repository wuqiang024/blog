# ViewPager相关
***

## 在主布局文件里加入ViewPager
***
```xml
<RelativeLayout ...>
  <ViewPager
    android:id="@+id/view_pager"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:layout_gravity="center" />
</RelativeLayout>
```

## 加载要显示的页卡
***
```java
List<View> viewList;
@Override
protected void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  setContentView(R.layout.acitivity_view_pager);
  LayoutInflater inflater = LayoutInflater.from(this);
  View view1 = inflater.inflate(R.layout.item0, null);
  View view2 = inflater.inflate(R.layout.item1, null);
  viewList = new ArrayList<>();
  viewList.add(view1);
  viewList.add(view2);
}
```

## 实例化ViewPager组件
***
```java
private class MyPageAdapter extends PagerAdapter {
  @Override
  public int getCount() {
    return viewList.size();
  }

  @Override
  public ifViewFromObject(View view, Object object) {
    return view == object;
  }

  @Override
  public Object instantiateItem(ViewGroup container, int position) {
    View view = viewList.get(position);
    container.addView(view);
    return view;
  }

  @Override
  public void destroyItem(ViewGroup container, int position, Object object) {
    container.removeView(viewList.get(position));
  }
}
```