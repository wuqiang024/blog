# 如何理解VDom?
***
曾经，前端常做的事情就是根据数据状态的更新，来更新界面试图。大家逐渐认识到，对于复杂试图的界面，频繁的更新DOM，会造成回流或者重绘，引发性能下降，页面卡顿。

因此，我们需要方法避免频繁的更新DOM树。思路也很简单，即：对比DOM的差距，只更新需要部分的节点，而不是更新一棵树。而实现这个算法的基础，就需要遍历DOM树的节点，来进行比较更新。

为了处理更快，不使用DOM对象，而是用JS对象来表示，他就像是JS和DOM之间的一层缓存。

# 如何表示VDom?
***
借助ES6的class,表示VDom语义化更强。一个基础的VDom需要有标签名，标签属性以及子节点，如下所示:

```js
class Element {
    constructor(tagName, props, children) {
        this.tagName = tagName;
        this.props = props;
        this.children = children;
    }
}
```

为了更方便调用(不用每次都写new)，将其封装返回实例的函数:

```js
function el(tagName, props, children) {
    return new Element(tagName, props, children);
}
```

此时，如果想表达下面的DOM结构:

```html
<div class="test">
    <span>span1</span>
</div>
```

用VDom表示就是:

```js
// 子节点数组的元素可以是文本，也可以是节点
const span = el('span', {}, ['span1']);
const div = el('div', {class: 'test'}, [span]);
```

之后在对比和更新两棵VDom树的时候，会涉及到将VDom渲染成真正的Dom节点，因此，为class Element增加render方法：

```js
class Element {
    constructor(tagName, props, children) {
        this.tagName = tagName;
        this.props = props;
        this.children = children;
    }

    render() {
        const dom = document.createElement(this.tagName);
        Reflect.ownKeys(this.props).forEach(name => {
            dom.setAttribute(name, this.props[name])
        });
        this.children.forEach(child => {
            const childDom = child instanceof Element ? child.render() : document.createTextNode(child);
            dom.appendChild(childDom);
        });
        return dom;
    }
}
```

# 如何比较VDom,并且进行高效更新?
***
前面已经说明了VDom的用法与含义，多个VDom就会组成一棵虚拟的DOM树，剩下需要做的就是: 根据不同的情况，来进行树上节点的增删改的操作，这个过程分别分为diff和patch:
* diff: 递归对比两VDom树的，对应位置的节点差异
* patch: 根据不同的差异，进行节点的更新。

目前两种思路，一种是先diff一遍，记录所有的差异，再统一进行patch；另外一种是diff的同时，进行patch，相较而言，第二种方法少了一次递归查询，以及不需要构造过多的对象，下面采用第二种思路。

## 变量的含义
将diff和Patch的过程，放入updateEl方法中，这个方法的含义如下:

```js
/**
 * 
 * @param {HTMLElement} $parent
 * @param {Element} newNode
 * @param {Element} oldNode
 * @param {Number} index
 * /
 
 function updateEl($parent, newNode, oldNode, index = 0) {
     /...
 }
 ```

 所有以`$`开头的变量，代表着真实的DOM

 参数index表示oldNode在$parent的所有子节点构成的数组中的下标位置。

 ## 情况一: 新增节点
 如果oldNode为undefined，说明newNode是一个新增节点，直接将其追加到DOM节点中即可。

 ```js
 function updateEl($parent, newNode, oldNode, index) {
     if(!oldNode) {
         $parent.appendChild(newNode.render());
     }
 }
 ```

 ## 情况二: 删除节点
 如果newNode为undefined，说明新的VDom树中，当前位置没有节点，因此需要将其从实际的DOM中删除。删除就用`$parent.removeChild()`，通过index参数，可以拿到被删除元素的引用。

 ```js
 function updateEl($parent, newNode, oldNode, index) {
     if(!oldNode) {
         $parent.appendChild(newNode.render());
     } else if(!newNode) {
         $parent.removeChild($parent.childNodes[index]);
     }
 }
 ```

 ## 情况三: 变化节点
 对比oldNode和newNode，有三种情况，均可视为改变:
 1、节点类型发生改变: 文本变vdom; vdom变文本
 2、新旧节点都是文本，内容发生改变
 3、节点的属性值发生改变
 首先，借助Symbol更好地语义化声明这三种变化

 ```js
 const CHANGE_TYPE_TEXT = Symbol('text');
 const CHANGE_TYPE_PROP = Symbol('props');
 const CHANGE_TYPE_REPLACE = Symbol('replace');
 ```

 针对节点属性发生改变，没有现成的api供我们批量更新，因此封装replaceAttribute，将新VDom的属性直接映射到dom结构上:

 ```js
 function replaceAttribute($node, removeAttrs, newAttrs) {
     if(!$node) {
         return;
     }
     Reflect.ownKeys(removedAttrs).forEach(attr => $node.removeAttribute(attr));
     Reflect.ownKeys(newAttrs).forEach(attr => {
         $node.setAttribute(attr, newAttrs[attr])
     })
 }
 ```

 编写`checkChangeType`函数判断变化的类型，如果没有变化，则返回空。

 ```js
 function checkChangeType(newNode, oldNode) {
     if(typeof newNode !== typeof oldNode || newNode.tagName !== oldNode.tagName) {
         return CHANGE_TYPE_REPLACE;
     }

     if(typeof newNode === 'string') {
         if(newNode !== oldNode) {
             return CHANGE_TYPE_TEXT;
         }
         return;
     }

     const propsChanged = Reflect.ownKeys(newNode.props).reduce((prev, name) => prev || oldNode.props[name] !== newNode.props[name], false);

     if(propsChanged) {
         return CHANGE_TYPE_PROP;
     }
     return;
 }