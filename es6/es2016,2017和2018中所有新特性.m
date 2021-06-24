# ES2016
## Array.prototype.includes
includes是数组上的一个简单实用的方法，可以轻松查找数组中是否有制定内容(包括NaN)。

## 求幂操作符
在ES2016中，引入了`**`代替Math.pow。
```js
Math.pow(7, 2)  // 49
7 ** 2 // 49
```

# ES2017
## Object.values()
Object.values()是一个类似于Object.keys()的新函数，但返回对象自身属性的所有值，不包括原型链中的任何值
```js
const cars = {BM2: 3, Tesla: 2, Toyota: 3};
Object.values(cars) // [3, 2, 3]
```

## Object.entries()
Object.entries()与Object.keys()类似，但他不仅是返回键，而是以数组方式返回键和值。
```js
Object.entries(cars) // [['BMW', 3], ['Tesla', 2], ['Toyota', 1]];
```
## 字符串填充
在String.prototype中添加了2个实例方法: String.prototype.padStart和String.prototype.padEnd,
允许在初始化字符串的开头或末尾追加/前置空字符或其他字符。
```js
'5'.padStart(10) // '         5'
'5'.padEnd(10, '=*') // '5=*=*=*=*='
```

## Object.getOwnPropertyDescriptors
此方法返回给定对象的所有属性的所有属性(包括getter setter set方法)，添加这个的主要目的是允许浅拷贝/克隆到另一个对象中的对象，类似Object.assign()。
Object.assign()浅拷贝除原始对象的getter和setter方法之外的所有属性。
Object.assign()和Objecy.getOwnPropertyDescriptors以及Object.defineProperties之间的区别，

## 函数参数的尾逗号
ES2017允许函数的最后一个参数有尾逗号，此前，函数定义和调用时，都不允许最后一个参数后面出现逗号。这一变化鼓励开发人员停止丑陋的"行以逗号开头"的习惯。

## Async/Await
async函数允许我们不处理回调地狱，并使得整个代码看起来很简单。
async关键字告诉JS编译器以不同的方式对待函数。每当编译器到达函数中的await关键字时，他会暂停。他假定wait之后的表达式返回一个promise，并在进一步移动之前
等待该promise被resolved或rejected。

`async函数默认返回一个promise`,如果你正在等待async函数的结果，则需要使用Promise的then语法来捕获其结果。
在以下示例中，我们希望使用console.log来打印结果但是不在doubleAndAdd函数里操作，因为async返回是一个promise对象，所以可以在then里面执行我们的一些操作。

```js
async function doubleAndAdd(a, b) {
    a = await doubleAfterSec(a);
    b = await doubleAfterSec(b);
    return a + b;
}
doubleAndAdd(1, 2).then(console.log);

function doubleAfterSec(param) {
    return new Promise((resolve, reject) => {
        setTimeout(resolve(param * 2), 1000);
    })
}
```

`并行调用async/await`
在前面的例子中，我们调用doubleAfterSec，但每一次我们等待一秒钟(总共2秒)。相反，我们可以使用Promise.all将他们并行为一个并行而且互不依赖。
```js
async function doubleAndAdd(a, b) {
    [a, b] = await Promise.all([doubleAfterSec(a), doubleAfterSec(b)]);
    return a + b;
}

doubleAfterSec(1, 2).then(res => {
    console.log(res);
})

function doubleAfterSec(param) {
    return new Promise(resolve => {
        setTimeout(resolve(param * 2), 1000)
    })
}
```

`async/await函数对错误的处理`
在使用async/await,有多种方法可以处理错误。
1、在函数内使用try-catch
2、在await后的promise语句后加catch捕获错误
3、在整个的async-await函数捕获错误

# ES2018
## 用于正则表达式的"dotall"标志
目前在正则表达式中，虽然点(".")应该匹配单个字符，但他不匹配像\n\t\f\r等新行字符
例如:
```js
/first.second/.test('first\nsecond'); // false
```
这种增强使点运算符能够匹配任何单个字符，为了确保他不破坏任何东西，我们需要在正则表达式时使用\s标志。
```js
// ES2018
/first.second/s.test('first\nsecond'); // true, Notice: /s

## RegExp Named Group Captures
这种增强RegExp特性借鉴于像Python，Java等语言，因此称为命名组，这个特性允许编写开发人员以(...)格式为RegExp中组的不同部分提供名称(标志符)，
使用可以用这个名称轻松的获取他们需要的任何组。

### Named group的基础用法
在下面的示例中，我们使用(?)名称对日期正则表达式的不同部分进行分组。结果发现现在将包含一个groups属性，该属性有year,month,day的相应值。
```js
let pattern = /(\d{4})-(\d{2})-(\d{2})/;
let result = pattern.exec('2015-01-02');
console.log(result);
// ['2015-01-02','2015','01','02',index:0,input:'2015-01-02']
let pattern = (?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/u;
let result = pattern.exec('2015-01-02');
console.log(pattern.exec(result));
// ['2015-01-02','2015','01','02',index:0,input:'2015-01-02',groups:{year:'2015',month:'01',day:'02'}]
console.log(result.groups.year) // '2015'
```

### 在regex内使用Named groups
使用\k<组名>格式来反向引用正则表达式本身中的组，例如:
```js
// 在下面的例子中，我们有一个包含的"水果"组
// 他既可以配苹果也可以配橘子
// 我们使用"\k<group name>" (\k<fruit>)来反向引用这个组的结果
let sameWords = /(?<fruit>apple|orange)=\k<fruit>/u;
sameWord.test('apple=apple') // true
sameWord.test('orange=orange') // true
sameWord.test('apple=orange') // false
```

### 在String.prototype.replace中使用Named groups
在String.prtototype.replace中使用Named groups。所以我们能更快捷的交换词。
例如，把"firstName,lastName"改成"lastName,firstName"
```js
let re = /(?<firstName>[A-Za-z]+) (?<lastName>[a-zA-Z]+$)/u;
'hello world'.replace(pattern, `$<lastName>, $<firstName>`);
```

## 异步迭代
这是一个极其好用的新特性。让我们能够非常r容易的创建异步循环代码。
```js
const promise = [
    new Promise(resolve => resolve(1)),
    new Promise(resolve => resolve(2)),
    new Promise(resolve => resolve(3))
];
// 使用for-of遍历不会等待每一个Promise resolve
async function test1() {
    for(let obj of promise) {
        console.log(obj); // promise, promise, promise
    }
}

// 使用for-await-of遍历会等待每一个promise resolve之后，进入下一次循环。
async function test2() {
    for await (let obj of promise) {
        console.log(obj); // 1, 2, 3
    }
}
```