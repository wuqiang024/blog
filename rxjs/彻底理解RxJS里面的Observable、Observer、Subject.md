# Observable和Observer
关于RXJS的基础概念，`observable`和`observer`，我们常常搞得头晕眼花。
其实，看下面这简简单单的一行代码就懂了他们的关系。

```js
observable.subscribe(observer);
```

observable是数据源头，是生产者，是待订阅者，通过subscribe方法可以被订阅，而observer是观察者，是消费者，数据使用者。

这句代码返回的是一个订阅对象，代表着一个订阅的发生，一个订阅的过程，一个Subscription对象的实例化。

observer其实是一个有三个回调函数的对象，每个回调函数对应observable发送的通知类型(next, error, complete)。回调函数不必每次提供三个，如果我们只提供了一个回调函数作为参数，subscribe会将我们提供的函数参数作为next的回调处理函数。

observable.subscribe()是一个Subscription对象。Subscription就是表示Observable的执行，可以被清理。这个对象最常用的方法就是unsubscribe方法。同时，他还有add方法可以使我们取消多个订阅。

我有一个比喻可以很好的理解这种关系: 现在有一家牛奶生产商，他们的牛奶物美价廉，他在电视上发布广告，所有人都可以打他们的电话订奶。这个时候，牛奶商就是Observable，市民就是Observer。如果市民打电话(subscribe)给牛奶商，他们就会在牛奶商送奶(next)成功的时候收到牛奶，至于怎么喝就是自己的事情了，而市民是不关心牛奶是怎么生产和如何送来的。送奶的过程可能会遇到意外而失败(error)，而成功之后，牛奶商会把这次牛奶标记为(complete)。

这些都是基础中的基础，即使有时候我们被他搞得头晕眼花，但是我们大概也知道他们的意思。而下面这个Subject。很多人不太理解。

我们常常搞不懂RXJS里面Subject的概念以及何时使用它。其实在官方文档的最开始，简单的HERO教程里，早就有这么一段。
![https://user-gold-cdn.xitu.io/2019/12/23/16f32180de6bbbf1?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/23/16f32180de6bbbf1?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

Subject其实是一个很有用，很优雅的东西。在RXJS官方文档，我们可以看到关于Subject的介绍。
![https://user-gold-cdn.xitu.io/2019/12/23/16f32183dc9a065b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1](https://user-gold-cdn.xitu.io/2019/12/23/16f32183dc9a065b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

后面还有这么一句话: Subject是将任意Observable执行共享给多个观察者的唯一方式。简单的说，Subject即是Observable，也是观察者(可以多个)。

我们知道，对于Observable来说，每个观察者有自己的订阅者的独立执行。什么意思呢? 比如说，有一个人订奶，就要有一个送奶的过程的发生；有一个Service里面的Get请求被订阅，就会发生一个Http请求。

这种模式在我们的某些情况下不太适合，比如说，输入框input change的过程，可能是毫秒之间，如果采用这个方式，我们需要创建多少个subscription对象? 或者牛奶丝做双十一促销活动，突然一秒钟就有一个订单产生，我们如果还采用一个一个送，需要多少个执行过程。

聪明的你应该想到了，那么一次送多份牛奶。这就是RXJS官方文档说的。Subject像是Observable。但是可以多播给多个观察者。Subject还像是EventEmitter。维护着多个监听器的注册表。

看看HERO教程里的应用。

```js
private searchTerms = new Subject<string>();
search(term: string): void {
	this.searchTerms.next(term);
}
```

searchTerms现在就是一个源源不断的能发出输入框值的流。即可不断的发出值，又可以使用subscribe源源不断的获得值。而这一切，通过Subject变得很简单。

Subject还有3个比较常用的子类: `ReplaySubject，AsyncSubject, BehaviorSubject`。他们代表什么意思？之间又有什么区别呢？

## Subject
代码例子

```js
import { Subject, ReplaySubject，AsyncSubject, BehaviorSubject } from 'rjjs';
let subject1: Subject<number> = new Subject<number>();
subject1.next(100);
subject1.subscribe(res => {
	console.log('subjectA:' + res);
})
subject1.subscribe(res => {
	console.log('subjectB:' + res）)
})
subject1.next(200);
subject1.next(300);
```

执行结果:
SubjectA: 200
SubjectB: 200
SubjectA: 300
SubjectB: 300

可见，Subject只有在订阅后，才能收到数据源发出的值。subject1.next(100)的时候，还没有被订阅，因此不会打印结果。如果我们想在订阅者创建后，无论什么时候都能拿到数据，这应该怎么办呢。下面的就派上用场了。

## BehaviorSubject
代码例子

```js
let subject2: BehaviorSubject<number> = new BehaviorSubject<number>(0);
subject2.next(100);
subject2.subscribe(res => {
	console.log('BehaviorSubjectA:' + res)
})
subject2.next(200);
subject2.subscribe(res => {
	console.log('BehaviorSubjectB:' + res)
})
subject2.next(300);
```

执行结果
BehaviorSubjectA: 100
BehaviorSubjectA: 200
BehaviorSubjectB: 200
BehaviorSubjectA: 300
BehaviorSubjectB: 300

可见，BehaviorSubject会保存最新的发送数据，当被订阅时，会立即使用这个数据。然后会继续接受新的值。BehaviorSubjectA发生订阅的时候，当前值是100，所以立即会打印100，然后她收到了新发出的200；这个时候BehaviorSubjectB订阅了，他会立即打印最新值200，然后A,B依次接受到了300.

需要注意的是: BehaviorSubject必须设置默认值，因为有一个最新值的概念。那么如果我们想保存所以的数据，而不只是最新值，怎么办呢?

## ReplaySubject
代码例子:

```js
let subject3: ReplaySubject<number> = new ReplaySubject<number>();
subject3.next(100);
subject3.next(200);
subject3.subscribe(res => {
	console.log('ReplaySubjectA:' + res);
})
subject3.next(300);
subject3.subscribe(res => {
	console.log('ReplaySubjectB:' + res)
})
subject3.next(400);
```

执行结果:
ReplaySubjectA: 100
ReplaySubjectA: 200
ReplaySubjectA: 300
ReplaySubjectB: 100
ReplaySubjectB: 200
ReplaySubjectB: 300
ReplaySubjectA: 400
ReplaySubjectB: 400

ReplaySubject会保存所有值，然后回放给订阅者。

这里的ReplaySubjectA订阅的时候，数据流里有100，200，之后接收300；这个时候新的订阅ReplaySubjectB发生了，数据流里有100，200，300，所以他会依次打印出这些已经保存的数据，然后A和B依次收到了400.

我们可以理解为，这些数据流全都会被保存下来，当有新的订阅发生时，像放电影一样回放给订阅者。

## AsyncSubject
AsyncSubject只有当Observable执行完成时(执行complete)，他才会将执行的最后一个值发送给观察者。

也就是说，他指挥保存流里的最后一条数据，而且只会在数据流complete时候发送。

```js
let subject4: AsyncSubject<number> = new AsyncSubject<number>();
subject4.next(100);
subject4.subscribe(res => {
	console.log('AsyncSubjectA:' + res);
})
subject4.next(200);
subject4.subscribe(res => {
	console.log('AsyncSubjectB:' + res);
})
subject4.next(300);
subject4.subscribe(res => {
    console.log('Async-SubjectC:' + res);
});
subject4.complete();
subject4.next(400)
```

执行结果
AsyncSubjectA: 300
AsyncSubjectB: 300
AsyncSubjectC: 300

可见，数据流在complete之前，有100，200，300，最后一条是300。所有订阅者都只会收到最后一条300.而complete之后，自然不会再发送值了。

## 附加知识
最后，其实Subject还有一个子类`AnonymousSubject`，只是这个子类很少有使用场景。
有时候我们想当然认为使用create可以实例化Subject，实际上，Subject.create()会返回AnonymousSubject对象实例，而new Subject()会返回Subject对象实例。AnonymousSubject不会像一般的Subject一样订阅自己。他会标记数据源，然后在订阅发生时，他会直接连接起数据源和观察者但是却不追踪我们创建的订阅的过程(即数据变化的过程)。比如:

```js
var timer$ = Rx.Observable.timer(1000, 2000);
var timerSubject = Rx.Subject.create(null, timer$);

var subscription1 = timerSubject.subscribe(n => console.log(n));
var subscription2 = timerSubject.subscribe(n => console.log(n));

setTimeout(() => timerSubject.unsubscribe(), 4000); // 不生效
```

这里的subscription1实际上是直接订阅了timer$，所以他其实是不可unsubscribe的。
