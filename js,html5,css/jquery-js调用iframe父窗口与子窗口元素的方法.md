# jquery、js调用iframe父窗口与子窗口元素的方法
***

## 在父页面获取iframe子页面的元素
***

`(在同域的情况下且在http://下测试，最好在iframe onload加载完后dosomething...)`

**js写法:**
**a、通过contentWindow获取**
也有通过contentDocument获取的，但是contentWindow兼容各个浏览器，可取得子窗口的window对象。
contentDocument Firefox支持，>IE8的ie支持。可取得子窗口的document对象。

获取方法:

```js
var frameWin = document.getElementById('iframe').contentWindow; // window对象
var frameDoc = document.getElementById('iframe').contentWindow.document; // document 对象
var frameBody = document.getElementById('iframe').contentWindow.document.body; // body对象
```

还有iframe.contentDocument方法，但是ie6,7不支持。

**b、通过iframes[]数组获取**
`(但是必须在iframe框架加载完毕后获取，iframe1是iframe的name属性)`

```js
document.getElementById('ifameId').onload = function() {
    var html = window.iframes['name属性'].document.getElementById('iframe中的元素的id').innerHTML;
}
```

**jquery写法:必须在iframe加载完后才有效**
**a**
```js
$('#iframe的ID').contents().find('#iframe中的控件ID').click(); // jquery 方法1 必须在iframe加载完后才有效
```

**b**
```js
$('#iframe中的控件ID', document.iframes('frame的name').document); // 方法2
```

**2、在iframe中获取父级页面的ID元素**
`(在同域的情况下并且在http://下测试，最好是iframe加载完毕再do something)`

**js写法**

```js
// 获取父级中的objid
var obj = window.parent.document.getElementById('#id')
```

`window.top`方法可以获取父级的父级的...最顶级的元素对象

**jquery写法**

```js
$('#父级窗口的objId', window.parent.document);  // window可省略不写
$(window.parent.document).find('#objid').css('height': height); // window可省略不写
```

## 父级窗口访问iframe中的属性
`(经测试，在ie中最好使用原生onload事件，如果用jq的load把iframe加载完毕，有时候方法调用不到，多刷新才有效果)`

```js
document.getElementById('iframe1').onload = function() {
    this.contentWindow.run()
}
```

```js
document.getElementById('iframe1').onload = function() {
    frames['frame1'].run();
}
```

## 在iframe中访问父级窗体的方法和属性 // window可以不写

```js
window.parent.attributeName; // 访问属性是在父级窗口中的属性名
window.parent.Func(); // 访问属性Func()是在父级窗口中的方法
```

## 让iframe自适应高度
```js
$('#iframeId').load(function() {
    var iframeHeight = Math.min(iframe.contentWindow.window.document.documentElement.scrollHeight, iframe.contentWindow.window.document.body.scrollHeight);
    var h = $(this).contents().height();
    $(this).height(h + 'px');
})

$('#iframeId').load(function() {
    var iframeHeight = $(this).contents().height();
    $(this).height(iframeHeight + 'px');
});
```

## iframe的onload事件
主流浏览器都支持iframe.onload = function() {};
在ie下需要用attachEvent绑定事件。

## 在iframe所引入的网址写入防钓鱼代码

```js
if(window != window.top) {
    window.top.location.href = window.location.href;
}
```

## 获取iframe的高度
iframe.contentWindow.document.body.offsetHeight;

**window.self**
对当前窗口的引用；self, window.self, window三者是等价的

**window.top**
对顶层窗口的引用，如果本身就是顶层窗口，则返回本身

**window.parent**
对父窗口的引用，如果没有父窗口，则返回本身。
