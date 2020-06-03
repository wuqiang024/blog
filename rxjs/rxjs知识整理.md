## 简介
rxjs的内容可以概况为一个核心三个重点，核心就是Observable和Operators，三个重点分别是:
* observer
* subject
* scheduler
其中众多的operator一直是我们学习rxjs路上的拦路虎，文章主题内容也将是围绕这部分内容讲解。

## 简单的例子
下面用一个简单的例子来展示rxjs如何工作

```js
var observable = Observable.create(function(observer) {
    observer.next('jerry');
    observer.next('Anna');
})

// 订阅observable
observable.subscribe(function(value) {
    console.log(v);
})
```

通过observable身上的create方法可以创建一个Observable，参数中的回调函数设置这个Observable将会如何传递值，然后通过subscribe订阅这个Observable。

> 这里值得一提的是rxjs的subscribe是同步执行的，例如下面这段代码。

```js
var observable = Observable.create(function(observer) {
    observer.next('jerry');
    observer.next('anna');
})

console.log('start');
observable.subscribe(function(v) {
    console.log(value);
});
console.log('end');
```

最终结果为

```js
start
jerry
anna
end
```

通过subscribe订阅启动的代码在第二个log之后才会在控制台打印，由此可以看出subscribe是同步执行的。

## rxjs的operators
学号operators是学会rxjs的关键，熟练使用rxjs中各种各样的operators可以大大提高我们的工作效率。

## operators的分类
![https://upload-images.jianshu.io/upload_images/5657516-692ef9b98afebb46.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp](https://upload-images.jianshu.io/upload_images/5657516-692ef9b98afebb46.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

### 创造observable类

`create`
```js
const observable = Observable.create(observer => {
    observer.next('value');
})
observable.subscribe({
    next: () => {},
    complete: () => {},
    error: () => {}
})
```

`of`
感觉Of类似一个迭代器，将参数迭代后输出
```js
var source = of('jerry', 'anna');
source.subscribe({
    next: (v) => {},
    complete: () => {},
    error: (error) => {}
});
```

`from`
from的参数必须是一个类数组(set, iterator)等，其他和of一样。
```js
var arr = [...];
var source = from(arr);
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`fromPromise`
遍历promise，和前两个一样
```js
var source = fromPromise(new Promise(resolve, reject) {
    setTimeout(() => {
        resolve('ok');
    }, 3000)
})

source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`fromEvent`
```js
var source = fromEvent(document.body, 'click');
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`empty`
empty会给我们一个空的observable，如果我们订阅这个observable，他会立即响应complete函数。
```js
var source = empty();

source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`throw`
他也只做一件事就是抛出错误
```js
source = throw('oop');
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`never`
数学上还有一个跟0很像的数，那就是无穷，在observable的世界里我们用never来建立无穷的observable,never会给我们一个无穷的observable，如果我们订阅他又会发生什么事情呢，什么事情都不会发生，他就是一个一直存在但却什么都不做的observable。

`interval`
interval和setInterval一样，几秒钟发送一个值，如下边代码所示:
```js
var source = interval(1000);
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
});
```

`timer`
有两个参数，第一个参数表示到发送第一个值的间隔时间，第二个参数表示从发送第二个参数开始，每发送一个值的间隔时间，如果第二个参数为空则发送第一个参数后，终止，执行complete函数。
```js
var source = Observable.timer(1000, 5000);
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

### 选择器类
`take`
有时候我们希望获取Observable的前几个数然后结束(执行complete方法)
```js
var source = interval(1000);
var example = source.pipe(take(3));
example.subscibe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})

`first` 获取第一个然后就结束，跟take(1)效果一样。
```js
source.pipe(first());
```

`takeLast`和`last`
takeLast和last用法一样，区别是该方法是取后边几个值,last是takeLast(1)的简写。目的是取最后一个值。

### 控制数据流类
`takeUntil`
参数为一个Observable，当参数Observable订阅发生，终止takeUntil绑定的observable。
下边这个案例，当点击body时就会终止订阅。
```js
const click = fromEvent(document.body, 'click');
const source = interval(1000).pipe(takeUntil(click));
source.subscribe({
    next: (value) => {},
    complete: () => {},
    error: (error) => {}
})
```

`skip`
使用方式类似take,take是取前几个，skip的意思是跳过前几个，取后边几个。
```js
const source = interval(1000).pipe(skip(3));
```
上面的例子跳过了前三个值，但是要注意的是获取前三个值的时间还是要等待的。

`startWith`
塞一个初始值给Observable

`concat`
concat和concatAll效果是一样的。区别在于concat要传递参数，参数必须是Observable类型。
concat将多个Observable串接起来，前一个完成好了再执行下一个。
```js
const source1 = interval(1000).pipe(take(3));
const source2 = of(3);
const source3 = of(4, 5);
const example = source1.pipe(concat(source2, source3));
```

`merge`
merge使用方式和concat一样，区别就是merge处理的Observable是异步执行的，没有先后顺序。
```js
const source1 = interval(1000).pipe(take(3));
const source2 = of(3);
const source3 = of(4, 5);
const example = source1.pipe(merge(source2, source3));
```

`delay`
delay会将observable第一次发出订阅的时间延迟，如下:
```js
const example = intervale(300).pipe(take(5), delay(500));
```

`delayWhen`
delayWhen和delay不同，他的延迟时间由参数函数决定，并且会将主订阅对象发出的值作为参数:
```js
var example = interval(300).pipe(take(5), delayWhen(x => empty().delay(100 * x));
```
上边的例子会将第一次source发出的值作为参数传给delayWhen的函数作为参数，只有在参数对象中的observalble发出订阅的值，主订阅对象才会继续发出订阅的值。

`debounceTime`
debounce在每次收到元素，他会先把元素cache住并等待一段时间，如果这段时间内已经没有收到任何元素，则把元素送出；如果在这段时间内又收到新的元素，则会把原本cache的元素释放掉并重新计时，不断反复。

`throttleTime`
跟debounce不同的是throttle会先开放发出元素，等到有元素被送出就会沉默一段时间，等到时间过了又会继续发出元素，防止某个事件频繁触发，影响效率。
```js
var source = intervale(300).pipe(take(5), throttleTime(1000));
source.subscribe({
    ...
});
// 输出 0, 4, complete
```

`distinct`
distinct会和已经拿到的数据进行比较过滤掉重复的元素。
```js
var source = from(['a', 'b', 'c', 'a', 'b']).pipe(zip(interval(300), (x, y) => x), distinct());
// a b c complete
```
distinct第一个参数是一个函数，函数返回值就是distinct比较的值。
```js
var soure = from([{value:'a'}, {value:'b'}, {value:'c'}, {value:'a'}, {value:'c'}]).pipe(zip(intervale(300), (x, y) =x ))
var example = source.pipe(distinct(x) => {
    return x.value
});
// {value: 'a'} {value: 'b'} {value: 'c'}
```
但是distinct底层是创建一个set来辅助去重，如果数据很大，可能导致set过大，这个时候需要设置distinct第二个参数来刷新set，第二个参数是个observable到发起订阅的时候就会清空set.
```js
var flushes = intervale(1300);
var example = from(['a', 'b', 'c', 'a', 'b']).pipe(zip(interval(500), (x, y) => x), distinct(null, flushes))
```

`distinctUntilChanged`与`distinct`不同，distinctUntilChanged只会比较相邻的两次输入，例子如下。
```js
var example = from(['a', 'b', 'c', 'c', 'b']).pipe(zip(interval(300), (x, y) => x), distinctUntilChanged());
// a b c b complete
```

### 协调多个Observable类
`combineLatest`
协调多个observable，参数Observable中有一个发生变化都会发起订阅(前提是每个observable都有值)。
```js
const timerOne = timer(1000, 4000);
const timerTwo = timer(2000, 4000);
const timerThree = timer(3000, 4000);
const combined = combineLatest(timeOne, timeTwo, timeThree);
const subscribe = combined.subscribe(latestValues => {
    const [timerValOne, timerValTwo, timerValThree] = latestValues;
    console.log(
        'Timer One Latest: ${timerValOne}',
        'Timer Two Latest: ${timerValTwo}',
        'Timer Three latest: ${timerValThree}'
    );
})
```
当combineLatest没有传入第二个参数，返回的订阅值是个数组，但是combineLatest可以传入第二个参数，在发给observable进行处理。

`zip`
和combineLatest用法基本一样，主要作用也是协调几个observable, zip的特定是只会取几个observable对应的index的值进行计算。例子如下:
```js
const source1 = interval(1000).pipe(take(3));
const source2 = interval(1000).pipe(take(3));
const example = source1.pipe(zip(source2, (x, y) => {
    return x + y;
}));
example.subscribe({});
// 0 2 4 complete
```

