# 前言
## 什么是RxJS
RxJS是ReactiveX编程理念的javascript版本。ReactiveX来自微软，是一种针对异步数据流的编程。简单来说，他可以将一切数据，包括HTTP请求，Dom事件或者普通数据等包装成流的形式，然后用强大丰富的操作符对流进行处理，使你能以同步编程的方式处理异步数据，并组合不同的操作符来轻松优雅的实现你所需的功能。

## RxJS可用于生产吗
ReactiveX由微软于2012年开源，目前各语言库由ReactiveX组织维护。RxJS在Github上有8000多个star,目前最新版本为5.5.2，并且持续开发中，其中官方测试用例共2699个。

## RxJS对项目代码的影响？
RxJS中的流以Observable对象呈现，获取数据需要订阅Observable，形式如下:

```js
const ob = http$.getSomeList();  // getSomeList()返回某个由Observable包装后的http请求
ob.subscribe((data) => console.log(data));
// 在变量末尾加$表示Observable类的对象
```

以上与Promise类似:

```js
const promise = http.getSomeList(); // 返回由Promise包装的http请求
promise.then((data) => console.log(data));
```

实际上Observable可以认为是加强版的Promise,他们之间是可以通过RxJS的API互相转换的。

```js
const ob = Observable.fromPromise(somePromise); // Promise转为Observable
const promise = someObservalbe.toPromise(); // Observable转为Promise
```

因此可以在Promise方案的项目中安全使用RxJS，并能够随时升级到完整的RxJS方案。

## RxJS会增加多少体积
RxJS(v5)整个库压缩后为140K，由于其模块化可扩展的设计，因此仅需导入所用到的类与操作符即可。导入RxJS常用类与操作符后，打包后的体积约增加30-60K，具体取决于导入的数量。

`不要用import { Observable } from 'rxjs'这种方式导入，这回导入整个rxjs库，按需导入的方法如下：`

```js
import { Observable } from 'rxjs/Observable'  // 导入类
import 'rxjs/add/operator/map' // 导入实例操作符
import 'rxjs/add/observable/forkJoin'  // 导入类操作符
```

## RxJS快速入门
### 初级核心概念
* Observable
* Observer
* Operator

Observable可称为可观察序列，简单来说数据就是在Observable中流动，你可以使用各种Operator对流进行处理。例如:

```js
const ob = Observable.interval(1000);
ob.take(3).map(n => n * 2).filter(n => n > 2);
```

第一步代码我们通过类方法创建了一个Observable序列，ob作为源会每隔1000ms发射一个递增的数据，即0 -> 1 -> 2。第二步我们使用操作符对流进行处理，take(3)表示只取源发射的前3个数据，取完3个数据后关闭源的发射；map表示将流中的数据进行映射处理，这里我们将数据翻倍，filter表示过滤掉出符合条件的数据。根据上一步map的结果，只有第二个，第三个数据保留下来。

上面我们已经使用同步编程创建好了一个流的处理过程，但此时ob作为源并不会立刻发射数据，如果我们在map中打印n是不会得到任何输出的，因为ob作为observable必须被订阅才能够触发上述过程。也就是subscribe(发布/订阅模式)。

```js
const ob = Observable.interval(1000);
ob.take(3).map(n => n * 2).filter( n => n > 0).subscribe(n => console.log(n));
```

结果:
```js
2 // 第二秒
4 // 第三秒
```

上面代码中我们给subscribe传入了一个函数，这其实是一种简写，subscribe完整的函数签名如下:

```js
ob.subscribe({
	next: d => console.log(d),
	error: err => console.error(err),
	complete: () => console.log('complete')
})
```

直接给subscribe传入一个函数会被当成是next函数。这个完整的包含3个函数的对象被称为observer(观察者)，表示的是对序列结果的处理方式。next表示数据正常流动，没有出现异常；error表示流中出错，可能是运行出错，http报错等；complete表示流结束，不再发射新的数据。在一个流的生命周期中，error和complete只会触发其中一个，next可以有多个。直到complte或error。

observer.next可以认为是Promise中then的第一个参数，observer.error对应第二个参数或者Promise的catch。

RxJS同样提供了catch操作符，err流入catch后，catch必须返回一个新的Observable。被catch后的错误流将不会进入observer的error函数，除非其返回的新observable出错。

```js
Observable.of(1).map(n => n.undefinedMethod()).catch(err => {
	// 此处处理catch之前发生的错误
	return Observable.of(0); // 返回一个新的序列，该序列为新的流
})
```

## 创建可观测序列

`Observable.of(...args)` 可以将普通JS数据转为可观测数据
`Observable.fromPromise(promise)` 将Promise转为Observable
`Observable.fromEvent(element, eventName)` 从Dom事件创建序列，例如Observable.fromEvent($input, 'click')
`Observable.ajax(url | AjaxRequest)` 发送http请求。
`Observable.create(subscribe)` 这个属于万能的创建方法，一般用于只提供了回调函数的某些功能或库。

## 合并序列
合并序列也属于创建序列的一种，例如有这样一个需求，进入某个页面后拿到了一个列表，然后需要对列表每一项发出一个http请求来获取对应的详细信息，这里我们把每个http请求作为一个序列，然后我们希望合并他。
合并有很多方式，例如N个请求按顺序串行发出(前一个结束再发后一个)； N个请求同时发出并要求全部到达后合并为数组，触发一次回调。N个请求同时发出，对每一个到达就触发一次回调。
如果不用RxJS，我们会比较难处理这么多情形，不仅实现麻烦，维护更困难。下面是使用RxJS对上述需求的解决方案。

```js
const ob1 = Observable.ajax('api/detail/1');
const ob2 = Observable.ajax('api/detail/2');
...
const obs = [ob1, ob2, ...];
```

1、N个请求按顺序串行发出(前一个结束再开始后一个)

```js
Observable.concat(...obs).subscribe(detail => console.log('每个请求都触发返回'))
```

2、N个请求同时并行发出，对于每一个到达就触发一次返回

```js
Observable.merge(...obs).subscribe(detail => console.log('每个请求都触发一次回调'));
```

3、N个请求同时发出并且要求全部到达后合并为数组，触发一次回调

```js
Observable.forkJoin(...obs).subscribe(detailArray => console.log('触发一次回调'));
```

## 使用RxJS实现搜索功能
搜索是前端开发中很常见的功能，一般是监听`<input />`的`keyup`事件，然后将内容发送到后台，并展示后台返回的数据。

```js
var text = document.getElementById('#text');
var inputStream = Rx.Observable.fromEvent(text, 'keyup')
							   .debounceTime(250) // 防抖动
							   .plunk('target', 'value') // 取值
							   .switchMap(url => Http.get(url)) // 将当前输入流转为http请求
							   .subscribe(data => render(data)); // 接收数据
```

## 个人总结的常用操作符
类操作符(通常为合并序列或从已有序列创建序列)
合并: `forkJoin, merge, concat`
创建: `of, from, fromEvent, fromPromise, ajax, throw`

实例操作符(对流中的数据进行处理或控制)
`map, filter, switchMap, toPromise, catch, take, takeUntil, timeout, debounceTime, distinctUntilchanged, plunk`
