# LayoutInflate的几种用法
***

## 获取LayoutInflate的三种方法。
***
```
LayoutInflate inflate = LayoutInflate.from(this);
LayoutInflate inflate = getLayoutInflate();
Layoutinflate inflate = (LayoutInflate) getSystemService(LAYOUT_INFLATE_SERVICE);
```

## inflate方法的三个参数
***
```
inflater.inflate(R.layout.name, parent, false)
```
* R.layout.name 代表用哪个布局xml
* parent代表将该xml挂在哪个ViewGroup下
* flase 代表是否自动挂载，一般来说默认false
