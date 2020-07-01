# 深入理解Shadow Dom v1
***
shadow DOM是一种解决文档对象模型中缺少的树封装方法。

网页通常使用来自外部源的数据和小部件，如果他们没有封装，那么样式可能会影响到HTML中不必要的部分，迫使开发人员使用特定的选择器和!important规则来避免样式冲突。

尽管如此，在编写大型程序时，这些努力似乎并不那么有效，并且大量时间被浪费在防止css和js的冲突上。Shadow DOM AP旨在通过提供封装DOM树的机制来解决这些问题。

Shadow DOM是用于创建web组件的主要技术之一，另外两个是自定义元素和HTML模板。web组件的规范最初是由google提出的，用于简化web小部件的开发。

虽然这三种技术旨在协同工作，不过你可以自由地分别使用每种技术。本教程的范围仅限于Shadow DOM。

## 什么是DOM
***
在深入了解什么是shadow DOM之前，了解DOM是什么非常重要.W3C文档对象模型(DOM)提供了一个平台和语言无关的应用编程接口，用于表示和操作存储在HTML和XML文档中的信息。

通过使用DOM，程序员可以访问，添加，删除，修改元素和内容。DOM将网页视为树结构，每个分支以节点结束，每个节点包含一个对象，可以使用JS等脚本语言对其进行修改。

文档:
```html
<html>
    <head>
        <title>sample document</title>
    </head>
    <body>
        <h1>heading</h1>
        <a href='http://www.baidu.com'>Link</a>
    </body>
</html>
```

此HTML的DOM如下:
![https://segmentfault.com/img/bVbsmQl?w=800&h=632](https://segmentfault.com/img/bVbsmQl?w=800&h=632)
此图中所有的框都是节点。
用于描述DOM部分的术语类似于现实世界中的家谱树:
* 给定节点上一级节点是该节点的父节点
* 给定节点下一级节点是该节点的子节点
* 具有相同父级的节点是兄弟节点
* 给定节点上方的所有节点称为该节点的祖先节点
* 最后，给定节点下方的所有节点都被称为该节点的后代

节点的类型取决于它所代表的的HTML元素的类型。HTML标记被称为元素节点，嵌套标签形成一个元素树。元素中的文本称为文本节点。文本节点可能没有子节点，你可以把它想象成一棵树的叶子。

为了访问树，DOM提供了一组方法，程序员可以用这些方法修改文档的内容和结构。例如当你写下`document.createElement('p')`时就是在使用DOM提供的方法。没有DOM,JS就无法理解HTML和XML文档的结构。

## 什么是shadow DOM
***
封装是面向对象编程的基本特性，它使程序员能够限制对某些对象组件的未授权访问。
在此定义下，对象以公共访问方法的形式提供接口作为与其数据交互的方式。这样对象的内部表示不能直接被对象的外部访问。

Shadow DOM将此概念引入HTML，它允许你将隐藏的，分离的DOM连接到元素，这意味着你可以使用HTML和CSS的本地范围。现在可以使用更通用的CSS选择器而不必担心命名冲突，并且样式不再泄漏或被应用于不恰当的元素。

实际上，shadow DOM正是库和小部件开发人员将HTML结构，样式和行为与代码的其他部分分开所需要的东西。

Shadow root 是shadow树中最顶层的节点，是创建Shadow DOM时被附加到常规DOM节点的内容。具有与之相关联的shadow root的节点称为shadow host。

你可以像使用普通DOM一样将元素附加到shadow root。链接到shadow root的节点形成shadow树。通过图表应该能够表达的更清楚。

![https://segmentfault.com/img/bVbsmQm?w=800&h=512](https://segmentfault.com/img/bVbsmQm?w=800&h=512)

术语light DOM通常用于区分正常DOM和shadow DOM。shadow DOM和light Dom被并称为逻辑DOM。light DOM与shadow DOM分离的点被称为阴影边界。DOM查询和CSS规则不能到达阴影边界的另一侧，从而创建封装。

## 创建一个shadow DOM
***
要创建一个shadow DOM,需要用Element.attachShadow()方法将shadow root附加到元素。
```js
var shadowRoot = element.attachShadow(shadowRootInit);
```

来看一个简单的例子:
```js
<div id="host"><p>Default text</p><div>
<script>
    const ele = document.querySelector('#host');
    const shadowRoot = ele.attachShadow({mode:'open'});
    const p = document.createElement('p');
    shadowRoot.appendChild(p);
    p.textContent = 'hello';
</script>
```

此代码将一个shadow DOM树附加到div元素，其id是host。这个树与div的实际子元素是分开的，添加到他之上的任何东西都将是托管元素的本地元素。

![https://segmentfault.com/img/bVbsmQA?w=800&h=187](https://segmentfault.com/img/bVbsmQA?w=800&h=187)

Chrome DevTools中的Shadow root。

注意#host中的现有元素是如何被shadow root替换的。不支持shadow DOM的浏览器将使用默认内容。

现在，在将CSS添加到主文档时，样式规则将不会影响shadow DOM。

```js
<div><p>light DOM</p></div>
<div id="host"><div>
<script>
    const elem = document.querySelector('#host');
    const shadowRoot = elem.attachShadow({mode:'open'});
    shadowRoot.innerHTML = '<p>Shadow DOM</p>';
</script>
<style>
    p {color: red}
</style>
```

在light DOM中定义的样式不能超过shadow边界。因此只有Linght DOM中的段落才是红色。

![https://segmentfault.com/img/bVbsmQB?w=699&h=256](https://segmentfault.com/img/bVbsmQB?w=699&h=256

相反，你添加到shadow DOM的css对于host元素来说是本地的，不会影响到DOM中其他的元素:

```js
<div><p>lingth DOM</p></div>
<div id="host"></div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode: 'open'});
    shadowRoot.innerHTML = '<p>shadow DOM</p><style>p { color: red }</style>';
</script>
```

![https://segmentfault.com/img/bVbsmQN?w=699&h=256](https://segmentfault.com/img/bVbsmQN?w=699&h=256)

你还可以将样式规则放在外部样式表中，如下所示:
```js
shadowRoot.innerHTML = `
    <p>shadow DOM</p>
    <link rel="stylesheet" href="style.css"`;
```

要获得shadowRoot附加到的元素的引用，要使用host属性:
```js
<div id="host"><div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    console.log(shadowRoot.host);
</script>
```

要执行相反操作并获取对元素托管的shadow root的引用，可以用元素的shadowRoot属性。
```js
<div id="host"></div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    console.log(host.shadowRoot);
</script>
```

## shadowRoot mode
***
当调用host.attachShadow()方法来附加shadow DOM时，必须通过传递一个对象作为参数来指定shadow DOM树的封装模式，否则会抛出一个TypeError。该对象必须具有mode属性，其值为open或closed。

打开的shadow root允许你使用host元素的shadowRoot属性从root外部访问shadow root的元素。如下所示:
```js
<div><p>light DOM</p></div>
<div id="host"></div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    shadowRoot.innerHTML = `<p>shadow dom</p>`;
    host.shadowRoot.querySelector('p').innerText = 'test';
    host.shadowRoot.querySelector('p').style.color = 'red';
</script>
```

但是如果Mode是'closed'，则尝试从root外部用JavaScript访问shadow root的元素时会抛出一个TypeError:
```js
host.shadowRoot.querySelector('p').innerText = 'test' // error
```

当mode属性为closed时，shadowRoot属性返回null。因为null值没有任何属性或方法，所以在他上面调用querySelector会导致TypeError。浏览器通常用关闭的shadow root来使某些元素的实现内部不可访问，而且不可从js更改。

要确定shadow DOM是处于open还是closed模式，你可以参考shadow root的mode属性:

```js
host = document.querySelector('#host');
shadowRoot = host.attachShadow({mode:'closed'})；
console.log(shadowRoot.mode); // closed
```

从表面上看，对于不希望公开其组件的shadow root的web组件作者来说，封闭的shadow DOM看起来非常方便，然而在实践中绕过封闭的shadow DOM并不难。通常完全隐藏shadow DOM所需的工作量超过了它的价值。

## 并非所有HTML元素都可以托管shadow DOM
***
只有一组有限的元素可以托管shadow DOM。下面列出了支持的元素。

| article | aside | blockquote |
| body | div | footer |
| h1 | h2 | h3 |
| h4 | h5 | h6 |
| header | main | nav |
| p | section | span |

尝试将shadow DOM树附加到其他元素会导致`DOMException`错误。例如:
```js
document.createElement('img').attachShadow({mode:'open'}); // DOMException
```

用<img>元素作为shadow host是不合理的，因此这段代码抛出错误并不奇怪。你可能会收到DOMException错误的另一个原因是浏览器已经用该元素托管了shadow DOM。

## 浏览器自动将shadow DOM附加到某些元素
***
Shadow DOM已经存在很长一段时间了，浏览器一直用它来隐藏元素的内部结构，比如<input>,<textarea>和<video>。
当你在HTML中使用<video>元素时，浏览器会自动将shadow DOM附加到包含默认浏览器控件的元素。但DOM中唯一可见的是<video>元素本身。

![https://segmentfault.com/img/bVbsmQX?w=800&h=101](https://segmentfault.com/img/bVbsmQX?w=800&h=101

要在Chrome中显示此类元素的shadow root,请打开chrome devtool，然后在elements部分，选择settings下方的`show user agent shadow DOM`:

![https://segmentfault.com/img/bVbsmQY?w=800&h=301](https://segmentfault.com/img/bVbsmQY?w=800&h=301)

选中`show user agent shadow dom`后，shadow root节点及其子节点将变为可见。以下是启用此选项后相同代码的显示方式。

![https://segmentfault.com/img/bVbsmQZ?w=800&h=327](https://segmentfault.com/img/bVbsmQZ?w=800&h=327

## 在自定义元素上托管shadow DOM
***
Custom Elements API创建的自定义元素可以像其他元素一样托管shadow DOM。
```js
<my-element></my-element>
<script>
    class MyElement extend HTMLElement {
        constructor() {
            super();
            const shadowRoot = this.attachShadow({mode:'open'});
            shadowRoot.innerHTML = `<style>p{color:red}</style><p>hello</p>`;
        }
    }
    customElements.define('my-element', MyElement);
</script>
```
此代码创建了一个托管shadow DOM的自定义元素。它调用了customElements.define()方法，元素名称作为第一个参数，类对象作为第二个参数。该类扩展了HTMLElement并定义了元素的行为。

在构造函数中，super()用于建立原型链，并且把shadow root附加到自定义元素。当你在页面上使用<my-element>时，他会创建自己的shadow dom.

请记住: 有效的自定义元素不能是单个单词，并且名称中必须包含连字符(-)。例如，myelement不能用作自定义元素的名称，并会抛出DOMException错误。

## 样式化host元素
***
通常要设置host元素的样式，你需要将css添加到light DOM,因为这是host元素所在的位置。但是如果你需要在shadow DOM中设置host元素的样式呢。

这就是host()伪类函数的用武之地。这个选择器允许你从shadow root中的任何地方访问shadow host。

```js
<div id="host"></div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    shadowRoot.innerHTML = `
        <p>shadow dom</p>
        <style>
            :host {
                display: inline-block;
                border: 1px solid #ccc;
                padding: 0 15px;
            }
        </style>`
</script>
```

请注意的是:host仅在shadow root中有效。还要记住，在shadow root之外定义的样式规则比:host 中定义的规则具有更高的特殊性。

例如: `#host { font-size: 16px; }`的优先级高于shadow DOM的`:host { font-size: 20px }`。实际上这很有用，这允许你为组件定义默认样式，并让组件的用户覆盖你的样式。唯一的例外是`!important`规则，他在shadow DOM中具有特殊性。

你还可以将选择器作为参数传递给:host(),这允许你仅在host与指定选择器匹配时才会定位host。换句话说。它允许你定位同一host的不同状态。

```css
:host(:focus) {}
:host(.blue) {}
:host([disabled]) {}
```

## 基于上下文的样式
***
要选择特定祖先内部的shadow root host，可以用:host-context()伪类函数。
```js
:host-context(.main) {
    font-weight: bold
}
```
只有当他是`.main`的后代时，此css代码才会选择shadow host:
```html
<div class="main">
    <div id="host"></div>
</div>
```

`:host-context()`对主题特别有用，因为它允许作者根据组件使用的上下文对组件进行样式设置。

## 样式钩子
***
shadow DOM的一个有趣的地方是他能够创建样式占位符并允许用户填充他们。这可以通过使用css自定义属性来完成。
```html
<div id="host"></div>
<style>
    #host{--size: 20px;}
</style>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    shadowRoot.innerHTML = `<p>shadow dom</p><style>p { font-size: var(--size, 16px)}</style>`;
</script>
```

这个shadow DOM允许用户覆盖其段落的字体大小。使用自定义属性表示法(--size:20px)设置该值，并且shadow DOM用var()函数(font-size:var(--size,16px))检索该值，在概念方面，类似于<slot>元素的工作方式。

## 可继承的样式
***
shadow DOM允许你创建独立的DOM元素，而不会从外部看到选择器可见性，但这并不意味着继承的属性不会通过shadow边界。
某些属性(如color,background和font-family)会传递shadow边界并应用于shadow树。因此，与iframe相比，shadow DOM不是一个非常强大的障碍。

```html
<style>
    div {
        font-size: 25px;
        text-transform: uppercase;
        color: red
    }
</style>
<div><p>light dom</p></div>
<div id="host"></div>

<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    shadowRoot.innerHTML = `<p>shadow dom</p>`;
</scipt>
```

解决方法很简单，通过声明`all: initial`将可继承样式重置为其初始值。
```js
shadowRoot.innerHTML = `
    <p>shadow dom</p>
    <style>
        :host p {
            all: initial;
        }
    </style>
```

在上例中，元素被强制回初始状态，因此穿过shadow边界的样式不起作用。

## 重新定位事件
***
在shadow DOM内触发的事件可以穿过shadow边界并冒泡到light DOM元素，但是event.target的值会自动更改，因此它看起来好像该事件源自其包含的shadow树而不是实际元素的host元素。

此更改称为事件重定向，其背后的原因是保留shadow DOM封装。

```html
<div id="host"></div>
<script>
    const host = document.querySelector('#host');
    const shadowRoot = host.attachShadow({mode:'open'});
    shadowRoot.innerHTML = `
        <ul>
            <li>one</li>
            <li>two</li>
            <li>three</li>
        </ul>`;
    document.addEventListener('click', (event) => {
        console.log(event.target);
    }, false);
</script>
```

当你单击shadow DOM中的任何位置时，这段代码会将`<div id="host">...</div>`记录到控制台，因此侦听器无法看到调度该事件的实际元素。
但是在shadow DOM中不会发生重定向，你可以轻松找到与事件关联的实际元素。

```js
const host = document.querySelector('#host');
const shadowRoot = host.attachShadow({mode:'open'});
shadowRoot.innerHTML = `
    <ul>
        <li>one</li>
    </ul>`;
shadowRoot.querySelector('ul').addEventListener('click', (event) => {
    console.log(event.target);
});
</script>
```

请注意，并非所有事件都会从shadow DOM传播出去，那些做的只是重新定位，但其他只是被忽略了。如果你使用自定义事件的话，则需要使用composed:true标志，否则事件不会从shadow边界冒出来。

## Shadow dom v0 和 v1
***
Shadow DOM规范的原始版本在chrome25中实现，当时称为Shadow DOM V0。该规范的新版本改进了Shadow DOM API的许多方面。

例如,一个元素不能再承载多个shadow DOM,而某些元素根本不能托管shadow DOM。违反这些规则会导致错误。

此外，Shadow DOM v1提供了一组新功能，例如打开shadow模式，后备内容等，你可以找到两者之间的全面比较。
参考文献:https://hayato.io/2016/shadowdomv1/#multiple-shadow-roots
https://www.w3.org/TR/shadow-dom/

## 浏览器对Shadow DOM V1 的支持
***
在撰写本文时，Firefox和Chrome已经完全支持Shadow DOM V1。不幸的是，Edge尚未实现v1,Safari只是部分支持。在https://caniuse.com/#feat=shadowdomv1可以查看提供了支持的浏览器的最新列表。

要在不支持Shadow DOM v1的浏览器上实现shadow DOM，可以用shadydom和shadycss polyfill。
https://github.com/webcomponents/shadydom
https://github.com/webcomponents/shadycss

## 总结
***
DOM开发缺乏封装一直是一个问题，Shadow DOM API为我们提供了划分DOM范围的能力，从而为这个问题提供了一个优雅的解决方案。

现在，样式冲突不再是一个令人担忧的问题，选择器也不会失控。Shadow DOM改变了小部件开发的游戏规则，能够创建从页面其余部分封装的小部件，并且不受其他样式表和脚本的影响，这是一个巨大的优势。

如前所述，Web组件由三个主要技术组成，而Shadow DOM是其中的关键部分。