# 使用<a>标签时，你可能会忽略的一个安全问题
***
在一个新窗口中打开链接是前端开发中一个很常见的逻辑，他可以将用户引导到一个新的域名。我们可以用`target=_blank`来实现这个功能。每个人都会在他的某个项目中使用过`target=_blank`。但是不确定是否每个人都知道这种用法的缺陷。

当一个外部链接使用了`target=_blank`的方式，这个外部链接会打开一个新的浏览器tab。此时，新页面会打开，并且和原始页面占用同一个进程。这也意味着，如果这个页面有任何性能上的问题，比如有一个很高的加载时间，这也会影响到原始页面的表现。如果你打开的是一个同域的页面，那么你将可以在新页面访问到原始页面的所有内容，包括`document`对象(`window.opener.document`)。如果你打开的是一个跨域的页面，你虽然无法访问到document，但是你依然可以访问到`location`对象。

这就意味着，如果在你的站点或文章中，嵌入了一个通过新窗口打开一个新页面的链接，这个页面可以使用`window.opener`，在一定程度上来修改原始页面。

怎样组织这种情况发生呢？在所有使用`target=_blank`打开新页面的链接上，加上`rel="noopener"`。

```javascript
<a href="https://www.sohu.com" rel="noopener"></a>
```

在使用了`rel="noopener"`后，当一个新页面通过一个链接打开后，新页面中的恶意javascript代码将无法通过`window.opener`来访问原始页面。这将保证新页面运行在一个单独的进程里。

在老浏览器中，你可以使用`rel=noreferer`属性，具有同样的效果。但是这样也会阻止referer header被发送到新页面。

```javascript
<a href="http://www.sohu.com" rel="noopener noreferer"></a>
```

在上面的例子中，当用户点击这个超链接进入到新页面后，新页面拿不到referer信息，这样意味着，新页面不知道用户是从哪里来的。

如果你是通过js中的`window.open`打开一个页面的话，上文所说的也适用，因为你也是打开了一个新的窗口。在这种情况下，你不得不清除掉`opener`对象：

```javascript
var newwindow = window.open();
newwindow.opener = null;
```

## 总结
***
试想一下，如果在a页面通过`window.open`打开了b页面，b页面中有一段代码`window.opener.location = 恶意网址`，这个时候，a会自动跳转到恶意网址。