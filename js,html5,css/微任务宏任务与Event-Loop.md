# 微任务、宏任务与EventLoop
***
首先，js是个单线程的脚本语言。

就是说在一行代码执行的过程中，必然不会存在同时执行的另一行代码，就像使用alert()以后进行疯狂的console.log，如果没有关闭弹框，控制台是不会显示出一条log的信息的。

亦或有些代码进行了大量计算，比方说在前端暴力破解密码之类的鬼操作，这就会导致后续代码一直在等待，页面处于假死状态，因为前面的代码没执行完。

所以如果全部代码都同步执行，会引发很严重的问题，比方说我们要从远端获取数据，难道要一直循环代码去判断是否拿到了返回结果么？

于是就有了异步事件的概念，注册一个回调函数，比如发送一个网络请求，我们告诉主程序等到接收到数据后通知我，然后我们就可以去做别的事情了。

然后在异步完成后，会通知到我们，但是此时程序可能正在做其他事情，所以即使异步完成了也需要在一旁等待，等到程序空闲下来才有时间去查看哪些异步已经完成了，可以去执行。

比如说打了个车，如果司机先到了，但是你手头还有点事要处理，这时司机是不可能自己开车离开的，一定要等到你处理完事情才能走。

## 微任务与宏任务的区别
***
这个就像是去银行办理业务一样，先要取号排队。
一般上面都会印着类似: “您的号码为xxx，前边还有xxx人”等字样。

因为柜员同时只能处理一个来办业务的客户，这时每个来办理业务的人就可以认为是银行柜员的一个宏任务来存在的，当柜员处理完当前客户的问题后，选择接待下一位，广播报号，也就是下一个宏任务开始。

所以多个宏任务合在一起就可以认为说有一个任务队列在这，里面是当前银行中所有排号的客户。任务队列中的都是已经完成的异步操作，而不是说注册一个异步任务就会被放到这个异步队列中，就像在银行中排号，如果叫到你的时候你不在，那么你当前的排号就作废了，柜员会选择直接跳过进行下一个客户的业务处理，等你回来后还需要重新取号排队。

而且在一个宏任务中，是可以添加一些微任务的，就像在柜台办理任务，前面的一位老大爷可能在存款，在存款业务办完后，柜员还会问他有没有其他要办理的业务，这时候大爷说要办一些理财的业务，柜员肯定不会说让大爷再去排队取号。所以本来快轮到你的宏任务，因为大爷临时添加的理财任务这个微任务而延后。

在当前宏任务的微任务没有执行完时，是不会去执行下一个宏任务的。

所以下面的代码片段:
```js
setTimeout(_ => console.log(4));

new Promise(resolve => {
    resolve();
    console.log(1);
}).then(_ => {
    console.log(3);
});

console.log(2);
```

setTimeout就是作为宏任务来存在的，而Promise.then则是由代表性的微任务，上述代码的执行顺序就是按照序号来的。

所有会进入的异步都是指的事件回调中的那部分代码
也就是说`new Promise`在实例化的过程中所执行的代码是同步进行的，而then中注册的回调才是异步执行的。
在同步代码执行完后才会去检查是否有异步任务完成，并执行相应的回调，而微任务又会在宏任务之前执行。

本来`setTimeout`已经设置了定时器(相当于取号)，然后在当前进程中又添加了一些Promise的处理(临时添加理财业务)。

所以进阶的，即使我们继续在Promise中实例化Promise，其输出也依然会早于setTimeout的宏任务：

```js
setTimeout(_ => console.log(4))

new Promise(resolve => {
  resolve()
  console.log(1)
}).then(_ => {
  console.log(3)
  Promise.resolve().then(_ => {
    console.log('before timeout')
  }).then(_ => {
    Promise.resolve().then(_ => {
      console.log('also before timeout')
    })
  })
})

console.log(2)
```

当然，实际情况下很少会简单的这么调用Promise的，一般都会在里面有其他异步操作，比如fetch,fs.readFile之类的操作。
而这些其实就相当于注册了一个宏任务，而非微任务了。

`PS在Promise/A+的规范中，Promise的实现可以是微任务，也可以是宏任务，但是普遍的共识表示,Promise应该是属于微任务阵营的。`

## 宏任务
***
|-#-| 浏览器 | Node |
|--|--|--|
| I/O | ok | ok |
| setTimeout | ok | ok |
| setInterval | ok | ok |
| setImmediate | null | ok |
| requestAnimationFrame | ok | null |

有些地方会列出来UI Rendering，说这个也是宏任务，可是在阅读了HTML规范文档后,发现这很显然是和微任务平行的一个操作步骤.
requestAnimation姑且也算是宏任务吧，requestAnimationFrame在MDN中的定义为，下次页面重绘前所执行的操作，而重绘也是作为宏任务的一个步骤来存在的，并且该步骤晚于微任务的执行。

## 微任务
***
|-#-| 浏览器 | Node |
|--|--|--|
| process.nextTick | null | ok |
| MutationObserver | ok | null |
| Promise.then catch finally | ok | ok |

## EventLoop是什么
***
上面一直在讨论宏任务，微任务，各种任务的执行。
但是回到现实，js是一个单线程的语言，同时不能处理多个任务，所以何时执行宏任务，何时执行微任务?我们需要有这样的一个判断逻辑存在。

每办理完一个业务，柜员就会问当前的客户，是否还有其他需要办理的业务。（检查还有没有微任务需要处理)
而客户明确告知说没有以后，柜员就会去查看后边还有没有等着办理业务的人。(结束本次宏任务，检查还有没有宏任务需要处理)
这个检查的过程是持续进行的，没完成一个任务都会进行一次，而这样的操作被称为Event Loop。

而且就如同上边所说的一样，没完成一个任务都会进行一次，即便这些事情是一个客户所提出的，所以可以认为微任务也存在一个队列，大致是这样一个逻辑:

```js
const macroTaskList = [
    ['task1'],
    ['task2'],
    ['task3','task4']
];

for(let macroIndex = 0; macroIndex < micorTaskList.length; macroIndex++) {
    const macroTaskList = macroTaskList[micorIndex];
    for(let macroIndex = 0; macroIndex < macroTaskList.length; macroIndex++) {
        const macroTask = macroTaskList[macroIndex];

        // 添加一个微任务
        if(macroIndex === 1) macroTaskList.push('special macro task');
        console.log(macroTask);
    }
    // 添加一个宏任务
    if(macroIndex === 2) macroTaskList.push(['special micro task'])
}
```

之所以使用两个for循环来表示，是因为在循环内部可以很方便的进行push之类的操作(添加一些任务)，从而使迭代的次数动态的增加。

以及还要明确的是，Event Loop只是负责告诉你该执行哪些任务，或者说哪些回调被触发了，真正的逻辑还是在进程中进行。

## 浏览器中的表现
***
在上边简单的说明了两种任务的区别，以及Event Loop的作用，那么在真实的浏览器中是什么表现呢？
首先要明确一点的是，宏任务必然是在微任务之后才执行的(因为微任务实际上是宏任务的其中一个步骤)

I/O这一项感觉有点笼统，有太多的东西可以称为I/O，点击一次BUTTON,上传一个文件，与程序产生交换都可以称为I/O。

假设有这样一个DOM结构:
```js
<style>
  #outer {
    padding: 20px;
    background: #616161;
  }

  #inner {
    width: 100px;
    height: 100px;
    background: #757575;
  }
</style>
<div id="outer">
  <div id="inner"></div>
</div>
```

```js
const $inner = document.querySelector('#inner');
const $outer = document.querySelector('#outer');

function handle() {
    console.log('click'); // 直接输出
    Promise.resolve().then(() => console.log('promise')); // 注册微任务
    setTimeout(() => console.log('timeout')); // 注册宏任务
    requestAnimationFrame(() => console.log('animationFrame')); // 注册宏任务
    $outer.setAttribute('data-random', Math.random()); // DOM属性修改，触发微任务
}

new MutationObserver(() => {
    console.log('observer');
}).observe($outer, {
    attribute: true
})

$inner.addEventListener('click', handler);
$outer.addEventListener('click', handler);
```

如果点击#inner，其执行顺序一定是: `click > promise > observer > click > promise > observer > animationFrame > animationFrame > timeout > timeout`

因为一次I/O创建了一个宏任务，也就是说在这次任务中会去触发handler。
按照代码中的注释，在同步的代码已经执行完后，这时候就会去查看是否有微任务可以执行，然后发现了Promise和MutationObserver这两个微任务，执行之。
因为click事件会冒泡，所以对应的这次I/O会触发两次handler函数(一次在Inner, 一次在outer)，所以会优先执行冒泡的事件(早于其他宏任务)，也就是说会重复上述的逻辑。
在执行完同步代码和微任务后，这时继续向后查找有没有宏任务。
需要注意的一点是，因为我们触发了setAttribute，实际上修改了Dom的属性，这会导致页面的重绘，而这个set的操作时同步执行的，也就是说requestAnimationFrame的回调会早于setTimeout的执行。

## 一些小惊喜
***
使用上述代码，如果将手动点击DOM元素的触发方式改为$inner.click()，那么会得到不一样的结果。
`click > click > promise > observer > promise > animationFrame > animationFrame > timeout > timeout`

与我们手动触发click的执行顺序不一样的原因是这样的，因为并不是用户通过点击元素实现的触发事件，而是类似dispatchEvent这样的方式，个人觉得并不能算是一个有效的I/O，在执行了一次handler回调注册了微任务，注册了宏任务后，实际上外边的$inner.click()并没有执行完。
所以在微任务执行之前，还要继续冒泡执行下一次事件，也就是说触发了第二次的handler。
所以输出了第二次click，等到这两次handler都执行完之后才会去检查有没有微任务，有没有宏任务。

两点需要注意的:
1、.click()的这种触发方式个人认为是类似于dispatchEvent,可以理解为同步执行的代码。
```js
document.body.addEventListener('click', ()=> console.log('click'))
document.body.click()
document.body.dispatchEvent('click')
console.log('done');
// click click done
```

2、MutationObserver的监听不会说同时触发多次，多次修改只会有一次回调被触发。
```js
new MutationObserver(() => {
    console.log('observer');
}).observe(document.body, {
    attribute: true
})

document.body.setAttribute('data-random', Math.random());
document.body.setAttribute('data-random', Math.random());
document.body.setAttribute('data-random', Math.random());
// 只会输出一次observer
```

这就像是去饭店点餐，服务员喊了三次，xx号的牛肉面，不代表她会给你三碗。

## 在Node中的表现
***
Node也是单线程，但是在处理Event Loop上与浏览器稍有不同。
就单从API层面上来理解，Node新增了两个方法可以使用: 微任务的process.nextTick以及宏任务的setImmediate。

### setImmediate与setTimeout的区别
***
在官方文档中的定义，setImmediate为一次EventLoop执行完后调用。
setTimeout则是通过计算一个延时时间后进行执行。

但是同时还提到了如果在主进程中直接执行这两个操作，很难保证哪个会先触发。
因为如果主进程中先注册了两个任务，然后执行这两个任务时间超过XXs,而这时定时器已经处于可执行回调的状态了。
所以会先执行定时器，而执行完定时器后才是结束了一次Event Loop，这时才会执行setImmediate。

```js
setTimeout(() => console.log('setTimeout'));
setImmediate(() => console.log('setImmediate'))
```

有兴趣的同学可以自己试验一下，执行多次真的会得到不同的结果。

但是如果后续添加一些代码后，就可以保证setTimeout一定会在setImmediate之前触发了。
```js
setTimeout(() => console.log('setTimeout'))
setImmediate(() => console.log('setImmediate'))

let countdown = 1e9

while(countdown--) { } // 我们确保这个循环的执行速度会超过定时器的倒计时，导致这轮循环没有结束时，setTimeout已经可以执行回调了，所以会先执行`setTimeout`再结束这一轮循环，也就是说开始执行`setImmediate`
```

如果在另一个宏任务中，必然是setImmediate先执行:
```js
require('fs').readFile(__dirname, () => {
    setTimeout(() => console.log('timeout'));
    setImmediate(() => console.log('immediate'))
})
// 如果使用一个设置了延迟的setTimeout也可以实现相同的效果
```

### process.nextTick
***
就像上边说的，这个可以认为是类似于一个Promise和MutationObserver的微任务实现，在代码执行过程中可以随时插入nextTick，并且会保证在下一个宏任务开始之前所执行。

在使用方面的一个最常见的例子就是一些事件绑定类的操作。

```js
class Lib extends require('events').EventEmitter {
    constructor() {
        this.super();
        this.emit('init');
    }
}

const lib = new Lib;
lib.on('init', () => {
    // 这里将永远不会执行
    console.log('init');
})
```
因为上述代码在实例化lib对象时是同步执行的，在实例化完成后马上发送了init事件。而这时在外层的主程序还没开始执行到lib.on('init')监听事件这一步。
所以导致发送事件时没有回调，回调注册后事件不会再次发送。

我们可以很轻松的使用process.nextTick来解决这个问题。

```js
class Lib extends require('events').EventEmitter {
    constructor() {
        this.super();
        process.nextTick(() => {
            this.emit('init')
        })
    }
}
```
这样会在主进程的代码执行完毕后，程序空闲时触发Event Loop流程查找有没有微任务，然后再发送init事件。

关于有的文章中提到的，循环调用process.nextTick会导致报警，后续的代码永远不会执行，这是对的。参见上边使用的双重循环实现的loop即可，相当于在每次for循环执行中都对数组进行了push操作。这样循环永远不会结束。

## 多提一嘴async/await
***
因为,async/await本质上还是基于promise的一些封装，而promise是微任务的一种。所以在使用await关键字与Promise.then效果类似。
```js
setTimeout(() => console.log(4));

async function main() {
    console.log(1);
    await Promise.resolve();
    console.log(3);
}
main()
console.log(2);
```

async函数在await之前的代码都是同步执行的，可以理解为await之前的代码属于new Promise时传入的代码，await之后的代码都是在Promise.then中的回调。