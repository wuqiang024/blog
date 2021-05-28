# ListView的item点击事件
***

## 单纯的点击事件
***
```java
listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
  @Override
  public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
    // countryList.get(position).getName(); 取数据的方式
  }
})
```

可以看到，我们使用了setOnItemClickListener()来为ListView注册了一个监听器，当用户点击了ListView中的任何一个条目时，就会回调onItemClick方法，在这个方法中可以通过position参数判断出用户点击的是哪一条数据。

## 长按点击事件
***
```java
listView.setOnLongItemClickListener(new AdapterView.OnLongItemClickListener() {
  @Overrice
  public void onLongItemClick(AdapterView<?> parent, View view, int position, long id) {
    return false;
  }
})
```

onLongItemClick有个boolean返回值，代表是否消费掉这个事件，当这个返回值为false的时候，处理完长按事件，还会处理条目的点击事件，如果返回为true，则处理完长按事件后，就不再处理点击事件了。

## 数据更新事件
***
```java
list.remove(position);
adapter.notifyDataSetChanged(); // 刷新界面
```