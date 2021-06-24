# 细数CSS伪元素及其用法
***
CSS中有两个很常见的概念，伪类和伪元素。
伪类用于在页面中的元素处于某个状态时，为其添加指定的样式。
伪元素会创建一个抽象的伪元素，这个元素不是DOM中的真实元素，但是会存在于最终的渲染树中，我们可以为其添加样式。

最常规的区分伪类和伪元素的方法是:实现伪类的效果可以通过添加类来实现，但是想要实现伪元素的等价效果只能创建实际的DOM节点。

此外，伪类使用单冒号`:`,伪元素使用双冒号`::`。

伪元素可以分为排版伪元素，突出显示伪元素，树中伪元素三类。

## 第一类: 排版伪元素
***
`1、::first-line伪元素`
表示所属源元素的第一格式化行。可以定义这一行的样式。
```js
p::first-line {
    text-decoration: uppercase;
}
<p>LSFSFS DSFSDFK SDdsdd ssdfdsf  sfsdfsfad</p>
```
第一格式化行被截断的位置与元素的宽度，字体大小等很多因素有关。

虽然在DOM中看不到，但实际上，上面的这段HTML代码会通过添加虚拟标签的方式进行修改。如下:
```html
<p><p::first-line>Lorem ipsum dolor sit amet consectetur adipisicing elit.</p::first-line> Necessitatibus quisquam ipsum sunt doloribus accusamus quae atque quaerat quam deleniti beatae, ipsam nobis dignissimos fugiat reiciendis error deserunt. Odio, eligendi placeat.</p>
```

如果`::first-line`伪元素的应用会截断真实的元素，这个时候会在截断的位置之后再重新添加开标签。
```js
<!-- 无伪元素 -->
 <p><span>Lorem ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus quisquam ipsum sunt doloribus accusamus quae atque quaerat quam deleniti beatae, ipsam nobis dignissimos fugiat reiciendis error deserunt.</span> Odio, eligendi placeat.</p>
 <!-- 有伪元素 -->
 <p><p::first-line><span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span></p::first-line><span> Necessitatibus quisquam ipsum sunt doloribus accusamus quae atque quaerat quam deleniti beatae, ipsam nobis dignissimos fugiat reiciendis error deserunt.</span> Odio, eligendi placeat.</p>
 ```

 `如何确定第一个格式化行`
 需要注意的是，`::first-line`伪元素只在应用的块级容器上才有效，而且必须出现在相同流的块级子孙元素中(即没有浮动和定位)。

 如下所示，DIV的首行就是P元素的首行。
 ```html
 <div>
 <p>Lorem ipsum</p> dolor sit amet consectetur adipisicing elit. Omnis asperiores voluptatem sit ipsa ex fugit provident tenetur eum pariatur impedit cumque corrupti iste expedita, esse nulla ad et excepturi. Iste!
 </div>
 <!-- 等价抽象代码 -->
 <div>
 <p><div::first-line>Lorem ipsum</div::first-line></p> dolor sit amet consectetur adipisicing elit. Omnis asperiores voluptatem sit ipsa ex fugit provident tenetur eum pariatur impedit cumque corrupti iste expedita, esse nulla ad et excepturi. Iste!
 </div>
 ```

 如果display值为`table-cell`和`inline-block`的元素的内容，不能作为祖先元素的第一个格式化行内容。

 如下所示，如果将上面HTML标签中的P标签改为`display: inline-block`，则其不会应用首行效果。

 ![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400ovDzAEJVN0CyUWNxfue9qibmw6qz3hAFjL4QVo6yricb4fkHicFuzww0w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400ovDzAEJVN0CyUWNxfue9qibmw6qz3hAFjL4QVo6yricb4fkHicFuzww0w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)


 `可以用于::first-line伪元素的样式`
 `::first-line`生成的伪元素的行为类似于一个行级元素，还有一些其他限制。主要有以下样式可以应用于其上。
 * 所有的字体属性
 * `color`和`opacity`属性
 * 可以应用于行级元素的排版属性
 * 文字装饰属性
 * 可以用于行级元素的行布局属性
 * 其他一些规范中特别指定可以应用的属性
 此外，浏览器厂商有可能额外应用其他属性。

 `2、::first-letter伪元素`
 `::first-letter`伪元素代表所属源元素的第一格式化行的第一个排版字符单元，且其前面不能有任何其他内容。

 `::first-letter`常用于下沉首字母效果

 如下，我们可以创建一个下沉两行的段落。第一种方法，是CSS-INLINE-3中引入的，浏览器尚不支持。我们可以通过第二种方法实现同样的效果。

 ```js
 <style>
 h3 + p::first-letter {
    float: left;
    display: inline-block;
    font-size: 32px;
    padding: 10px 15px;
 }
 </style>
 <p>“Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos hic vero reprehenderit sunt temporibus?
 Doloribus consequatur quo illo porro quae recusandae autem eos. Corrupti itaque alias nam eius animi illum.</p>
 ```

 注意，第一个排版字符单元前的标点符号(可以是多个标点符号)也要包含在`::first-letter`伪元素内，CSS3 TEXT中规定，一个排版字符单元可以包含超过一个的Unicode码点。不同的语言也可以有额外的规则决定如何处理。

 如果将要放入`::first-letter`伪元素的字符不在同一个元素中，如`<p>"<em>L`中的`"L`,浏览器可以选择一个元素创建伪元素，也可以两个都创建，或者都不创建。

 在Chrome下效果如下，还是挺奇怪的。所以应尽量避免。
 ![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400Xqr6fffjhc3MNzKtr4evfs70BLXtnic7jMh25rPSUWJlfEvprsomqyw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400Xqr6fffjhc3MNzKtr4evfs70BLXtnic7jMh25rPSUWJlfEvprsomqyw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

 `2.1 如何确定首字母`
 首字母必须出现在第一格式化行内。

 如下所示，将`b`标签改为`display: inline-block`，则其不会出现在第一格式化行内，所以字母无效果。

 ```js
 <p>“<b style="display: inline-block;">Lorem</b>” ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos hic vero reprehenderit sunt temporibus?
 Doloribus consequatur quo illo porro quae recusandae autem eos. Corrupti itaque alias nam eius animi illum.</p>
```

![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400qF7MSK4sATNibRibnfm4osiaE6QkG2q13zZOmnlWULRKDTvw08zPWe3sA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400qF7MSK4sATNibRibnfm4osiaE6QkG2q13zZOmnlWULRKDTvw08zPWe3sA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

目前,`::first-letter`只可用于块级元素，未来可能会允许应用到更多的display类型中。

伪元素的虚拟标签应当紧跟在首字母之前，哪怕这个首字母是在子孙元素，这一点和`::first-line`类似。

如下例，首字母在子孙元素中，首字母并没有加粗，因为伪元素是添加到span标签内部的，所以字重是正常的。

```js
p { line-height: 1.1 }
p::first-letter { font-size: 2em; font-weight: normal }
span { font-weight: bold }
<p><span>Lorem ipsum</span> dolor sit amet consectetur adipisicing elit. Magni possimus rerum eaque architecto, adipisci neque odio, recusandae sapiente placeat ullam velit ratione esse aut expedita quae earum. Velit, dignissimos accusamus?</p>
```

![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400G2Vd41QSpGumPTjHictics9L5Ga6F4yvFduaxqmZtuAMXwqTKAXWickDQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400G2Vd41QSpGumPTjHictics9L5Ga6F4yvFduaxqmZtuAMXwqTKAXWickDQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

如果元素有`::before`或`::after`，则`::first-letter`伪元素也可以应用到其`content`值中。

如果元素是列表项(即`display: list-item`)，则首字母会应用在标记符号之后。如下图:

![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400DmvIhNNDTiciaLkBg2JuvetNP3kCLsiaticJuW6sW0E5aBRgMILoGQspSg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400DmvIhNNDTiciaLkBg2JuvetNP3kCLsiaticJuW6sW0E5aBRgMILoGQspSg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`2.2 可以用于::first-letter伪元素的样式`
`::first-line`生成的伪元素的行为类似于一个行级元素，还有一些其他限制。主要有以下样式可以应用于其上。
* 所有的字体属性
* color和opacity属性
* 所有的背景属性
* 可以应用于行级元素的排版属性
* 文字装饰属性
* 可应用于行级元素的行布局属性
* margin和padding属性
* border和box-shadow
* 其他一些规范中特别指定可以应用的属性

## 第二类: 突出显示伪元素
***
突出显示伪元素表示文档中特定状态的部分，通常采用不同的样式展示该状态。如页面内容的选中。
突出显示伪元素不需要在元素树中有体现，并且可以任意跨越元素边界而不考虑其嵌套结构。

突出显示伪元素不需要在元素树中有体现，并且可以任意跨越元素边界而不考虑其嵌套结构。

突出显示伪元素主要有以下几类：
1、`::selection`与`::inactive-selection`
这两个伪元素表示用户在文档中选取的内容。`::selection`表示有效的选择，相反，`::inactive-selection`表示无效的选择(如当前窗口无效，无法响应选中事件时)
如下图所示，我们可以定义页面选中内容的样式，输入框中的内容也可以。
![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400PHOaCNQmfTAIf10kjyOdSxtiao7dKlaHUicJOxvxqia8anq0pNOT0LUMQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400PHOaCNQmfTAIf10kjyOdSxtiao7dKlaHUicJOxvxqia8anq0pNOT0LUMQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

2、`::spelling-error`表示浏览器识别为拼写错误的文本部分。暂无实现

3、`::grammar-error`表示浏览器识别为语法错误的文本部分。暂无实现

`可以应用到突出显示类伪元素的样式`
对于突出显示类伪元素，我们只可以应用不影响布局的属性。如下:
* color
* background-color
* cursor
* caret-color
* text-decoration
* text-shadow
* stroke-color / fill-color / stroke-width

## 第三类: 树中伪元素
***
这类伪元素会一直存在于元素树中，它们汇集成源元素的任何属性。

1、内容生成伪元素: `::before/::after`
当`::before/::after`伪元素的`content`属性不为`none`时，这两类伪元素就会生成一个元素，作为源元素的子元素，可以和DOM树中的元素一样定义样式。

`::before`是在源元素的实际内容前添加伪元素。`::after`是在源元素的实际内容后添加伪元素。

正如上文提到的，与常规元素一样，`::before`和`::after`两个伪元素可以包含`::first-line`和`::first-letter`。

2、列表项标记伪元素: `::marker`
`::marker`可以用于定义列表项标记的样式。
如下: 我们可以分开定义列表项及其内容的颜色。
```html
<style>
    li { color: red; }
    li::marker { color: green }
</style>
<ul>
    <li>item 1</li>
</ul>
```

![https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400k1RmeuPdXE5J50p3HiaBzXsvliaWA0gQy6aVWHJtWvoBulUEgSqg36TA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/MpGQUHiaib4ib7LXgX9v1ZqBNsl5JojD400k1RmeuPdXE5J50p3HiaBzXsvliaWA0gQy6aVWHJtWvoBulUEgSqg36TA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`该伪元素暂时只有safari支持，尝试的话请使用safari。可以用于该伪元素的属性也有限，包括所有字体样式，color以及text-combine-upright，有待以后扩充。`

3、输入框占位元素: `::placeholder`
`::placeholder`表示输入框内占位提示文字。可以定义其样式。
如:
```css
::placeholder { color: blue }
```
所有可以应用到`::first-line`伪元素的样式都可以用于`::placeholder`上。


