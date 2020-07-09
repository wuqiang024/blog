# 深度解析new原理及模拟实现
***
`new 运算符创建一个用户定义的对象类型的实例或具有构造函数的内置对象的实例。`

```js
function Car(color) {
    this.color = color;
}
Car.prototype.start = function() {
    console.log(this.color);
}

var car = new Car('black');
car.color; // 访问构造函数的属性
car.start(); // 访问原型里的属性
```

可以看出`new`创建的实例有以下两个特征:
* 1、访问到构造函数里的属性
* 2、访问到原型里的属性

注意点:
ES6新增的Symbol类型，不可以使用`new Symbol()`，因为`Symbol`是个基本类型，每个从`Symbol()`返回的symbol值都是唯一的。

`模拟实现`
当代码new Foo()执行时，会发生以下事情:
* 1、一个继承自Foo.prototype的新对象被创建
* 2、使用指定的参数调用构造函数Foo,并将this绑定到新创建的对象。`new Foo`等同于`new Foo()`，也就是没有指定参数列表，Foo不带任何参数调用的情况。
* 3、由构造函数返回的对象就是new 表达式的结果。如果构造函数没有显示返回一个对象，则使用步骤一创建的对象。

`模拟实现第一步`
`new`是关键词，不可以直接覆盖，这里使用`create`来模拟实现`new`的效果。
`new`返回一个对象，通过`obj.__proto__=Con.prototype`继承构造函数的原型，同时通过`Con.apply(obj, arguments)调用父构造函数实现继承，获取构造函数上的属性。

实现代码如下:

```js
function create() {
    var obj = new Object(); // 创建一个空的对象
    Con = [].shift.call(arguments);
    obj.__proto__ = Con.prototype;
    Con.apply(obj, arguments); // 绑定this实现继承，obj可以访问到构造函数的属性
    return obj;
}
```

`模拟实现第二步`
构造函数返回值有如下三种情况:
* 1、返回一个对象
* 2、没有return，默认返回undifined
* 3、返回undefined以外的基本类型

`情况一`返回一个对象。
```js
 function Car(color, name) {
     this.color = color;
     return {
         name: name
     }
 }
var car = new Car('black', 'BMW');
car.color; // undefined
car.name; // BMW
```

实例car中只能访问到返回对象中的属性。

`情况二:没有return，即返回undefined`
```js
function Car(color, name) {
    this.color = color;
}
var car = new Car('black', 'BMW');
car.color; // black
car.name; // undefined
```

实例car只能访问到构造函数中的属性。

`情况三:返回undefined以外的基本类型`
```js
function Car(color, name) {
    this.color = color;
    return 'new Car';
}
var car = new Car('black', 'BMW');
car.color; // black
car.name; // undefined
```

实例car中只能访问到构造函数中的属性，和情况一完全相反，结果相当于没有返回值。

所以需要判断一下返回的值是不是一个对象，如果是对象则返回这个对象，不然返回新创建的obj对象。

```js
function create() {
    var obj = new Object();
    Con = [].shift.call(arguments);
    obj.__proto__ = Con.prototype;
    var ret = Con.apply(obj, arguments);
    return typeof ret === 'object' ? ret : obj;
}
```
