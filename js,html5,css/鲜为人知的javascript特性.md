# 鲜为人知的javascript特性
***

## void运算符
***
Javascript提供了一个一元运算符，你可能已经看到过他的这种用法，比如void(0)或void 0。他的作用只有一个--计算其右边的表达式并返回undefined。使用0只是一种惯例，你不一定要使用0，可以是任何有效的表达式，如void，他仍然会返回undefined。

```js
void(0)
void (0)
void 'abc'
void {}
void ( 1 == 1)
void ( 1 != 1 )
void anyFunction()
```

为什么要创建一个特殊的关键字来返回undefined，而不是直接返回undefined？这似乎有点多余。

实际上，在ES5之前，你可以在大多数浏览器中给undefined赋值，比如`undefined='ab'`。在那个时候，使用void是一种可以确保总是能够返回undefined的方法。

## 构造函数的括号是可选的
***
在调用构造函数的时候，类后面的括号是可选的(`前提是你不需要传递任何参数`)!
下面的代码都是有效的JS语法，并且会给你完全相同的结果!

```js
const date = new Date();
const month = new Date().getMonth();
const myInstance = new MyClass();

cosnt date = new Date;
const month = (new Date).getMonth();
const myInstance = new MyClass();
```

## 可以跳过IIFE的括号
***
IIFE(立即调用函数表达式)的语法有点奇怪，那些括号都有神马用途。
那些额外的括号只是为了告诉JS解析器，后面的代码是一个函数表达而不是一个函数。知道了这一点，我们就有很多方法跳过这些额外的括号，并仍然可以使用有效的IIFE.

```js
// IIFE
(function(){})()

void function(){}()
```

void运算符告诉解析器后面的代码是个函数表达式。因此我们可以跳过函数定义周围的括号。我们还可以使用任何一元运算符(void,+,!等)，他们都是有效的。

你可能会想，一元运算符不会影响IIFE返回的结果吗？

它确实会影响返回的结果。但如果你关心结果，并希望将结果赋值给某个变量，那么首先你就不需要额外的括号。

```js
// IIFE with a return
result = (function(){})();

result = function(){}()
```

我们添加这些括号只是为了更好的可读性。

## Function构造函数
***
function语句并不是定义函数的唯一方法，你可以使用Function()构造函数和new 运算符动态定义函数。

```js
const multiply = new Function('x', 'y', 'return x*y;');
multiy(2, 3)
```

最后一个参数是函数的字符串化代码，前面的其他参数是函数的参数。

Funtion构造函数是javascript中所有构造函数的祖先。甚至Object的构造函数也是Function。而Function自己的构造函数也是Function本身。因此如果调用object.constructor.constructor足够多的次数，最后将获得Function构造函数。

## 函数属性
***
我们都知道，函数是javascript的一等对象。因此，我们当然可以向函数添加自定义属性。这样做是完全有效的，然后，他很少被这样用。

那么，我们为什么会这么做呢?

`可配置的函数`
假设我们有一个叫greet的函数，我们希望它能够根据不同的区域设置打印出不同的问候语。区域设置也应该是可配置的。我们可以在某处维护一个全局区域环境变量，或者我们也可以使用函数属性来实现这个函数。如下所示。

```js
function greet() {
    if(greet.locale == 'fr') {
        console.log('Bonjour')
    } else if(greet.locale == 'es') {
        console.log('hola')
    } else {
        console.log('hello')
    }
}

greet() // hello
greet.locale = 'fr';
greet() // 'Bonjour'
```

`具有静态变量的函数`
另一个类似的例子，假设你想要实现一个生成一系列有序数字的数字生成器。通常你会使用Class或IIFE,并使用一个静态计数器变量来跟踪最后一个值。这样我们就可以限制对计数器的访问，并避免使用额外的变量来污染全局命名空间。

但是，如果我们希望能够灵活地读取甚至修改计数器，并且不污染全局命名空间呢？

我们仍然可以创建一个Class，带有一个计数器和一些额外的方法来读取他。或者我们可以使用函数的属性。

```js
function generateNumber() {
    if(!generateNumber.counter) {
        generateNumber.counter = 0;
    }
    return ++generateNumber.counter;
}

generateNumber() // 1
generateNumber() // 2
generateNumber.counter // 2
generateNumber.counter = 10
generateNumber.counter // 10
generateNumber() // 11
```

## 参数属性
***
相信大多数人都知道函数的arguments对象，他是一种类似数组的对象，所有函数都包括了他，他包含了调用函数时传给函数的所有参数，但是他也有一些有趣的属性:

* arguments.callee => 指当前调用的函数
* arguments.callee.caller => 指调用当前函数的函数

```js
const myFunction = function() {
    console.log(arguments.callee.name) // myFunction
    console.log(arguments.callee.caller.name) // main
}
```
注意: 尽管ES5禁止在strict模式下使用caller和callee，但在很多编译库中仍然很常见。

## ~运算符
***
没有人会关心位运算符，因为我们几乎很少使用他，但是他确实有一些使用场景。
当与数字一起使用时，比如~N => -(N+1)。这个表达式只在N == -1时结果为0.
我们可以在indexOf函数前加一个~来进行布尔检查，看看一个项是否存在于String或Array中。

```js
let username = 'Naht Drake';
if(~username.indexOf('Drake')) {
    console.log('ok')
} else {
    console.log('error')
}
```

注意: ES6和ES7分别在String和Array中添加了一个新的includes()方法。当然他比使用~运算符检查项目是否存在于Array或String中更清晰一些。

## +号运算符
***
快速将字符串转为数字。只需在字符串前添加+号即可。
加号运算符也适用于负数，八进制，十六进制，指数。他甚至可以将Date或Moment.js对象转换为时间戳。

## 逗号运算符
***
Javascript提供了一个逗号运算符，我们可以用它在一行中编写由逗号分隔的多个表达式，并返回最后一个表达式的结果。
`let result = expression1, expression2, ... expressionN`
这里所有的表达式都会被计算，并将expressionN返回的值赋值给result变量。
你可能已经在for循环中使用了逗号运算符:

```js
for(var a = 0, b = 10; a <= 10; a++, b--)
```

有时候，在一行中编写多个语句会有所帮助:

```js
function getNextValue() {
    return counter++, console.log(counter), counter
}

const getSquare = x => (console.log(x), x * x);
```

## 标记模板字面量
***
模板字面量是ES6的众多很酷的补充特性之一。但是，你知道标记模板字面量吗？

```js
myTag`Hello ${username}!`
```

在使用标记模板字面量的时候，你可以通过向模板字面量添加自定义标记来更好的控制如何将模板字面量解析为字符串。标记只是一个解析器函数，他获取字符串模板中所有的字符串和值，标记函数负责返回最终的字符串。

在下面的示例中，我们的自定义标记--highlight，解释模板字面量的值，并使用元素将解释的值包装在结果字符串中。以突出显示。

```js
function highlight(strings, ...values) {
    let result = '';
    strings.forEach((str, i) => {
        result += str;
        if(values[i]) {
            result += `<mark>${values[i]}</mark>`
        }
    })
    return result
}
```