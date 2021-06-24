# 一次弄懂EventLoop
***
EventLoop即事件循环，是指浏览器或Node的一种解决javascript单线程运行时不会阻塞的一种机制，也就是我们经常使用异步的原理。

## 为啥要弄懂Event Loop
***
* 增加自己技术的深度，也就是懂得javascript的运行机制
* 现在前端技术层出不穷，掌握底层原理，可以让自己以不变应万变
* 应对各大互联网公司的面试，懂其原理，题目任其发挥

## 堆、栈、队列
***
### 堆
***
堆是一种数据结构，是利用完全二叉树维护的一组数据，堆分为两种，一种为最大堆，一种为最小堆，根节点最大的堆称为最大堆或大根堆，根节点最小的堆称为最小堆或小根堆。
堆是线性数据结构，相当于一维数组，有唯一后继。

如最大堆
![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApBXqPdzouJWqucBicmmg1Dl0jGRicUMibytMnfZibUqAtPPszL4DeWI5LhA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApBXqPdzouJWqucBicmmg1Dl0jGRicUMibytMnfZibUqAtPPszL4DeWI5LhA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 栈
***
栈在计算机科学中是限定仅在表尾进行插入和删除操作的线性表。栈是一种数据结构，他按照先进后出的原则存储数据，先进的数据被压入栈底，最后的数据在栈顶，需要读数据的时候从栈顶开始弹出数据。
栈是只能在某一端插入和删除的特殊线性表。

![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApoSOyHicjZnEZdkxZpr0lMiaiaQPmu6HgX9aoAZtwZrupToMYMkXIkzFLQ/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApoSOyHicjZnEZdkxZpr0lMiaiaQPmu6HgX9aoAZtwZrupToMYMkXIkzFLQ/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 队列
***
特殊之处在于他只允许在表的前端进行删除操作，而在表的后端进行插入操作，和栈一样，队列是一种操作受限制的线性表。
进行插入操作的端称为队尾，进行删除操作的端称为队头。队列中没有元素时称为空队列。

队列的数据元素又称队列元素。在队列中插入一个队列元素称为入队，从队列中删除一个元素称为出队。因为队列只允许在一端删除，所以只有最早进入队列的元素才能最先从队列中删除，所以队列又称FIFO(先进先出)。

![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApxU4n7EamxDSDKsxzUlaujNWOR7XFN4Fswt3KWbNvzrGPctFfoVibhgA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApxU4n7EamxDSDKsxzUlaujNWOR7XFN4Fswt3KWbNvzrGPctFfoVibhgA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## Event Loop
***
在JavaScript中，任务分为两种，一种宏任务(MacroTask)也叫Task，一种叫微任务(MicroTask)。

### MacroTask(宏任务)
* script全部代码，`setTimeout`,`setInterval`,`setImmediate`(浏览器暂不支持，只有IE10支持),`I/O`,`UI Rendering`

### MicroTask(微任务)
***
* `process.nextTick(Node独有)`、`Promise`、`Object.observer(废弃)`、`MutationObserver`

## 浏览器中的Event Loop
***
JavaScript有一个main thread主线程和call-stack调用栈(执行栈)，所有任务都会被放到调用栈等待主线程执行。

### JS调用栈
***
JS调用栈采用的是后进先出的规则，当函数执行的时候，会被添加到栈的顶部，当执行栈完成后，会被从栈顶移出，直到栈内被清空。

### 同步任务和异步任务
***
JavaScript单线程任务分为同步任务和异步任务，同步任务会在调用栈中按照顺序等待主线程依次执行，异步任务会在异步任务有了结果后，将注册的回调函数放入任务队列中等待主线程空闲的时候(调用栈被清空)，被读取到栈内等待主线程的执行。

![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsAp27v9bVWSyjO18ljtSaM6fyicj9dPSxJKKUuJze4yiaEicJLqk1JDQ9oAA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsAp27v9bVWSyjO18ljtSaM6fyicj9dPSxJKKUuJze4yiaEicJLqk1JDQ9oAA/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

任务队列Task Queue即队列，是一种先进先出的数据结构。

![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApHznTdQxxv2H34s4icERfkk4ja4B9Rwrq6t6IPsKG4Dgrc70RvYlL0Pg/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApHznTdQxxv2H34s4icERfkk4ja4B9Rwrq6t6IPsKG4Dgrc70RvYlL0Pg/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 事件循环的进程模型
***
* 选择当前要执行的任务队列，选择任务队列中最先进入的任务，如果任务队列为空即null，则执行跳转到微任务的执行步骤
* 将事件循环中的任务设置为已选择任务
* 执行任务
* 将事件循环中当前任务设置为null
* 将已经完成的任务从任务队列删除
* microtask步骤: 进入microtask检查点
* 更新界面渲染
* 返回第一步

### 执行进入microtask检查点时，用户代理会执行以下步骤
***
* 设置microtask检查点标志位true
* 当事件循环microtask执行不为空时：选择一个最先进入的microtask队列的microtask，将事件循环的microtask设置为已选择的microtask，运行microtask,将已经执行完成的microtask设置为Null,移出microtask中的microtask。
* 清理IndexDB事务
* 设置进入microtask检查点的标志位false

![https://mmbiz.qpic.cn/mmbiz_gif/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApG0eFNeNp5LEvXxEMGjHJyqiaeNiczSaibem97v6yqVDQHPiasKzPWtPb6Q/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1](https://mmbiz.qpic.cn/mmbiz_gif/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApG0eFNeNp5LEvXxEMGjHJyqiaeNiczSaibem97v6yqVDQHPiasKzPWtPb6Q/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

执行栈在执行完同步任务后，查看执行栈是否为空，如果执行栈为空，就会去检查微任务队列是否为空，如果为空的话，就执行宏任务，否则就一次性执行完所有微任务。
每次单个宏任务执行完后，检查该宏任务下的微任务队列是否为空，如果不为空的话，会按照先进先出的原则全部执行完微任务。设置微任务队列为null，然后再执行宏任务，如此循环。

### 举个例子
```js
console.log('start');
setTimeout(function() {
    console.log('setTimeout');
})
Promise.resolve().then(function() {
    console.log('promise1');
}).then(function() {
    console.log('promise2');
})
console.log('end');
```

先执行script宏任务，打印出start,发现宏任务setTimeout，把它加入到宏任务队列中，再往下执行，发现Promise then,都属于微任务，把他们一次加入到script宏任务的微任务队列中，继续往下执行，打印end，此时执行栈已经清空，再去查找script宏任务下的微任务队列，依次执行promise1和promise2，此时，script下的微任务队列执行完毕，清空队列，去宏任务队列中去执行宏任务setTimeout，打印出setTimeout。因此结果是`start,end,promise1,promise2,setTimeout`

### 再举个例子
***
```js
console.log('start');
async function async1() {
    await async2();
    console.log('async1 end');
}

async function async2() {
    console.log('async2 end');
}

async1();

setTimeout(function() {
    console.log('setTimeout');
})

new Promise(resolve => {
    console.log('promise');
    resolve();
}).then(function() {
    console.log('promise1')
}).then(function() {
    console.log('promise2')
})
console.log('end')
```

这里需要先理解async/await。
async/await在底层转换成了promise和then回调函数。
也就是说，这是个promise的语法糖。
每次我们使用await，解释器都创建一个promise对象，然后把剩下的async函数中的操作放到then回调函数中。
async/await的实现，离不开promise。从字面意思来理解，async是异步的简写，而await是async wait的简写，可以认为等待异步方法执行完成。

### 关于73以下版本和73版本的区别
***
* 在73版本以下，先执行promise1和promise2，再执行async1。
* 在73版本，先执行async1再执行promise1和promise2

主要原因是因为在谷歌(金丝雀)73版本中更改了规范，如下图所示:

![https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApbDYkFRZETG1UE1xdWT4YJaIJpUY2Trlzib9jx8lqGlz3GyFooXfBenQ/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz/MpGQUHiaib4ib7ctqPcVg0mjZxaHQ0gUsApbDYkFRZETG1UE1xdWT4YJaIJpUY2Trlzib9jx8lqGlz3GyFooXfBenQ/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

* 区别在于RESOLVE(thenable)和之间的区别`Promise.resolve(thenable)`。

### 在73以下版本中
* 首先，传递给awati的值被包裹在一个Promise之后。然后，处理程序附加到这个包装的Promise，以便在Promise变为fulfiled后恢复该函数，并且暂停执行异步函数，一旦promise变为fulfiled，恢复异步函数的执行。
* 每个await引擎必须创建两个额外的Promise(即使右侧已经是一个promise)，并且他需要至少三个microtask队列ticks(tick为系统的相对时间单位，也被称为系统的时基，来源于定时器的周期性中断(输出脉冲), 一次中断表示为一个tick，也被称为一个时钟滴答，时标)

引用知乎上的一个例子:

```js
async function f() {
    await p;
    console.log('ok');
}
```

简化理解为
```js
function f() {
    return RESOLVE(p).then(() => {
        console.log('ok')
    })
}
```

* 如果RESOLVE(P)对于P的promise直接返回P的话，那么p的then方法就会马上被调用，其回调就立即进入job队列。
* 而如果RESOLVE(P)严格按照标准，应该是产生一个新的promise，尽管该promise确定会resolve为P,但这个过程是异步的，也就是现在进入job队列的是新promise的resolve过程，所以该promise的then不会立即调用，而要等到当前job队列执行到前述resolve过程才会被调用，然后其调用(也就是继续await之后的语句)才加入job队列，所以时序上就晚了。

