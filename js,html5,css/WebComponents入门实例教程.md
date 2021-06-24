# Web Components入门实例
***
组件是前端的发展方向，现在流行的React和Vue都是组件框架。
谷歌公司由于掌握了Chrome浏览器，一直在推动浏览器的组件化，即Web Componenta API。相比第三方框架，原生组件简单直接，符合直觉，不用加载任何外部代码，代码量小。目前，它还在不断发展，但已经可用于生产环境。

## 一、自定义元素
***
![https://www.wangbase.com/blogimg/asset/201908/bg2019080405.jpg](https://www.wangbase.com/blogimg/asset/201908/bg2019080405.jpg)

上图是一个用户卡片。
本文演示如何把这个卡片，写成Web Components组件。

网页只要插入下面的代码，就会显示用户卡片。

```html
<user-card></user-card>
```

这种自定义的HTML标签，称为自定义元素。根据规范，自定义元素的名称必须包含连词线，用于区别原生的HTML元素。所以<user-card>不能写成<usercard>。

## 二、customElements.define()
***
自定义元素需要用JavaScript定义一个类，所有<user-card>都会是这个类的实例。

```js
class UserCard extends HTMLElement {
    constructor() {
        super();
    }
}
```
上面代码中,UserCard就是自定义元素的类，注意，这个类的父类是HTMLElement，因此继承了HTML元素的特性。
接着，使用浏览器原生的customElement.define()方法，告诉浏览器<user-card>元素与这个类关联。
`window.customElements.define('user-card', UserCard);

## 三、自定义元素的内容
***
自定义元素<user-card>目前还是空的。下面在这个类里给出这个元素的内容。
```js
class UserCard extends HTMLElement {
    constructor() {
        super();
        
        var image = document.createElement('img');
        image.src = 'http//www.baidu.com/images/test.png';
        image.classList.add('image');

        var container = document.createElement('div');
        container.classList.add('container');

        var name = document.createElement('p');
        name.classList.add('name');
        name.innerText = 'User Name';

        var email = document.createElement('p');
        email.classList.add('email');
        email.innerText = 'youremail@.com';

        var button = document.createElement('button');
        button.classList.add('button');
        button.innerText = 'Follow';

        container.append(name, emai, button);
        this.append(image, container);
    }
}
```
上面代码最后一行，this.append()的this表示自定义元素实例。
完成这一步以后，自定义元素的内部结构就已经生成了。

## 四、<template>标签
***
使用JavaScript写上一节的DOM结构很麻烦，Web Components API提供了<template>元素，可以在它里面使用HTML定义DOM。

```html
<template id="userCardTemplate">
    <img src="http://www.sohu.com/test.png" class="image">
    <div class="container">
        <p class="name">User Name</p>
        <p class="email">Email</p>
        <button class="button">Follow</button>
    </div>
<template>
```

然后，改写一下自定义元素的类，为自定义元素加载<template>。

```js
class UserCard extends HTMLElement {
    constructor() {
        super();
        var templateElem = document.getElementById('userCardTemplate');
        var content = templateElem.content.cloneNode(true);
        this.appendChild(content);
    }
}
```

上面代码中，获取<template>节点以后，克隆了它的所有子元素，这是因为可能有多个自定义元素的实例，这个模板还要留给其他实例使用，所以不能直接移动它的子元素。

到这一步为止,完整代码如下。

```html
<body>
    <user-card></user-card>
    <template>...</template>

    <script>
        class UserCard extends HTMLElement {
            constructor(){
                super();
                var templateElem = document.getElementById('userCardTemplate');
                var content = templateElem.content.cloneNode(true);
                this.appendChild(content);
            }
        }
        window.customElements.define('user-card', UserCard);
    </script>
</body>
```

## 五、添加样式
***
自定义元素还没有样式，可以给它指定全局样式，比如下面这样。

```css
user-card {
    /* ... */
}
```

但是，组件的样式应该和代码封装在一起，只对自定义元素生效，不影响外部的全局样式，所以，可以把样式写在<template>里面。

```html
<template id="userCardTemplate"> 
    <style>
        :host { dipslay: flex }
        .image {}
        .container {}
    </style>

    <img class="image">
    <div class="container">
        <p class="name"></p>
        <p class="email"></p>
        <button class="button">Follow</button>
    </div>
</template>
```

上面代码中，<template>样式里面的:host伪类，指代自定义元素本身。

## 六、自定义元素的参数
***
<user-card>内容现在是在<template>里设定的，为了方便使用，把它改成参数。

```html
<user-card
    image="http://www.baidu.com/test.png"
    name="user name"
    email="youremai@email.com">
</user-card>
```

<template>代码也相应改造。

```html
<template id="userCardTemplate">
    <style></style>

    <img class="image">
    <div class="container">
        <p class="name"></p>
        <p class="email"></p>
        <button class="button">Follow john</button>
    </div>
</template>
```

最后改一下类的代码，把参数加到自定义元素里面。

```js
class UserCard extends HTMLElement {
    constructor() {
        super();

        var templateElem = document.getElementById('userCardTemplate');
        var content = templateElem.content.cloneNode(true);
        content.querySelector('img').setAttribute('src', this.getAttribute('image'));
        content.querySelector('.container>.name').innerText = this.getAttribute('name');
        content.querySelector('.container>.email').innerText = this.getAttribute('email');
        this.appendChild(content);
    }
}
window.customElements.define('user-card', UserCard);
```

## 七、Shadow DOM
***
我们不希望用户看到<user-card>的内部代码，Web Component允许内部代码隐藏起来，这叫做Shadow DOM，即这部分DOM默认与外部DOM隔离，内部任何代码都无法影响外部。

自定义元素的this.attachShadow()方法开启Shadow DOM，详见下面代码。

```js
class UserCard extends HTMLElement {
    constructor() {
        super();
        var shadow = this.attachShadow({mode:'open'});
        
        var templateElem = document.getElementById('userCardTemplate');
        var content = templateElem.content.cloneNode(true);
        // 同上
        shadow.appendChild(content);
    }
}
window.customElements.define('user-card', UserCard);
```

上面代码中，this.attachShadow()方法的参数{mode: 'closed'}表示shadow是封闭的，不允许外部访问。
至此，这个Web Component组件就完成了，完整代码可以看这里。可以看到，整个过程还是很简单的，不像第三方框架那样有复杂的API。

## 八、组件的扩展
***
在前面的基础上，可以对组件进行扩展。

1、与用户互动
用户卡片是一个静态组件，如果要与用户互动，也很简单，就是在类里监听各种事件

```js
this.$button = shadow.querySelector('button');
this.$button.addEventListener('click', () => {});
```

2、组件的封装
上面的例子中，<template>与网页代码放在一起，其实可以用脚本<template>注入网页，这样的话，JavaScript脚本跟<template>就能封装成一个JS文件，成为独立的组件文件，网页只要加载这个脚本，就能使用<user-card>组件。

更多高级用法，可以参考以下两篇文章。

https://www.robinwieruch.de/web-components-tutorial/
https://developers.google.com/web/fundamentals/web-components/customelements