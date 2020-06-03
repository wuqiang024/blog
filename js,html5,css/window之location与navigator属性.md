# window之location、navigator
## location对象
* location对象为全局对象window的一个属性，并且window.location = document.location，其中的属性都是可读写的，但是只有修改href和hash才有意义，href会重新定位到一个URL，hash会跳到当前页面中的anchor名字的标记(如果有),而且页面不会被重新加载。

```js
// 这行代码会使当前页面重定向
window.location.href = 'http://www.baidu.com';

// 如果使用hash并且配合input输入框，那么当页面刷新后，鼠标将会自动聚焦到对应id的input输入框。
<input type="text" id="target">
<script>
    window.location.href = '#target';
</script>
```

先看下其拥有的属性.

![https://user-gold-cdn.xitu.io/2020/4/21/1719d5465e6deae5?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2020/4/21/1719d5465e6deae5?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

这里补充一个origin属性，返回`URL协议+服务器名称+端口号(location.origin = location.protoco + '//' + location.host);` 

* 可以通过上述属性来获取URL中的指定部分，或者修改href与hash达到重新定位与跳转
* 添加hash改变监听器，来控制hash改变时执行的代码。

```js
window.addEventListener('hashchange', funcRef);
// 或者
window.onhashchange = funcRef;
```

location方法

| 方法名 | 说明 |
| ---- | ---- |
| assign() | 跳转链接，立即打开新的URL并在浏览器的历史记录中生成一条记录，回退可返回 |
| replace() | 跳转链接，立即打开新的URL，不会在历史记录中生成一条记录，回退不可返回 |
| reload() | 重新加载当前显示的页面: 参数: 无 ---- 就会使用最有效的方式重新加载页面，可能从浏览器缓存中重新加载。参数: true --- 那么就会强制从服务器重新加载 |

## navigator对象

* window.navigator对象包含有关浏览器的信息，可以用它来查询一些关于运行当前脚本的应用程序的相关信息。

```js
navigator.appCodeName // 浏览器的代码名，只读，在任何浏览器中，总是返回'Gecko'。该属性仅仅是为了保持兼容性
navigator.appName // 只读，返回浏览器的官方名称，不要指望会返回正确的值
navigator.appVersion // 同上
navigator.platform // 只读，返回一个字符串，表示浏览器所在的系统平台
navigator.product // 只读，返回当前浏览器的产品名称
navigator.userAgent // 只读，返回当前浏览器的用户代理字符串。