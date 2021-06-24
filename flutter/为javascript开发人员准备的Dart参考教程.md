# 为javascript开发人员准备的Dart教程
***
Dart是flutter主要的开发语言，这一篇主要是为JavaScript开发人员准备的Dart教程。
使用es2015作为参照；

示例可以使用`https://dartpad.dartlang.org/`来运行；Dart与JavaScript有非常重要的不同，Dart2开始他变成了一个强类型语言，JavaScript开发人员可以类比你在使用TypeScript。

## 常量和变量
***
`javascript`
```js
var c = 1;
c = 2;
let a = 1;
a = 2;
```

`dart`
```js
int a = 1;
a = 2;
var h = 1;
h = 2;
```

`常量`
```js
const b = 1; // js

final b = 1; // dart
const ggg = 1; // dart
```

final和const唯一的区别是final可以接收一个变量，但const不行，多数情况下我们会使用final来定义只赋值一次的值；

## 函数
***
定义函数:
```js
// JavaScript
function a(){}
const b = function(){}


// Dart
void funcs() {}
final funcs = (){}
```

多数情况下Dart函数和JS函数都有一样的特性，如:
* 将函数当做参数传递
* 将函数直接赋值给变量
* 对函数进行解构，只传递给函数一部分参数来调用它，让他返回一个函数去处理剩下的参数
* 创建一个可以被当做为常量的匿名函数

当你要使用一个非常简单的函数时，比如只返回一个字符串，它的表现形式和JS的箭头函数非常的像:
```js
// JS
const d = () => 'dd';

// Dart
String d() => 'dd';
```

实际上它可以等价为:
```js
// JS
const d = () => {
    return 'dd';
}

// Dart
String d() {
    return 'dd'
}
```

## 字符串模板
***
JS的模板和Dart一样，都是一个表达式；
```js
// JS
const d = 'icepy';
`hello ${d}`;

function dd() {
    return 'dd';
}
`hello ${dd()}`;

// Dart
final d = 'icepy'; 'hello ${d}';
String dd() => 'dd'; 'hello ${dd()}';
```

## 模块导入导出
***
JS使用了import 和 export来导入导出模块，Dart也使用了import来导入模块，只不过它和JS有一个显著的区别，Dart并不需要使用export来导出模块。
```js
// JS
import xxx from 'xxx';
import * as xx from 'xxx';
import { xx } from 'xxx';

// Dart
import 'package:xxx/xxx';
import 'package:xxx/xxx' show xxx; // 导出其中一个对象
import 'package:xxx/xxx' hide xxx; // 导出模块时不导出xxx;
import 'package:xxx/xxx' as myxxx; // 给导出的模块加上别名
```

## 类
***
为了更好的用语言描述你的程序，类就是这样一个很好的媒介，与JS非常一致的是Dart也使用class来定义一个类，使用extends来完成继承，与JS不同的是Dart有着更丰富的功能。

### 构造函数
***
```js
// JS
class Icepy {
    constructor(a) {
        this.a = a;
    }
}

// Dart
class Icepy {
    int a;
    Icepy(this.a);
}
```

### 构造函数参数默认值
***
```js
// JS
class Icepy {
    constructor(a = 1) {
        this.a = a
    }
}

// Dart
class Icepy {
    int a;
    Icepy({this.a = 1});
}

void main() {
    final i = new Icepy();
    print(i.a);
}
```

### 定义实例方法
***
```js
// JS
class Icepy {
    constructor(a = 1) {
        this.a = a;
    }
    say() {
        console.log(this.a);
    }
}

// Dart
class Icepy {
    int a;
    Icepy({this.a = 1});

    void say() {
        print(this.a);
    }
}

void main() {
    final i = new Icepy();
    i.say()
}
```

### 定义静态方法
***
```js
// JS
class Icepy {
    static staticMethod {
        return 'static';
    }
}

// Dart
class Icepy {
    int a;
    Icepy({this.a = 1});
    Icepy.stt() {
        print('2')
    }
}

void main() {
    Icepy.stt();
}
```

### getter & setter
***
```js
// JS
class Square {
    constructor(length) {
        this.name = 'Square';
    }
    get area() {
        return 2*2;
    }
    set area(value) {
        this._area = value;
    }
}

// Dart
class Rectangle {
    num left, top, width, height;
    Rectangle(this.left, this.top, this.width, this.height);
    num get right => left + width;
    set right(num value) => left = value - width;
    num get bottom => top + right;
    set bottom(num value) => top = value - height;
}

void main() {
    var rect = new Rectangle(3, 4, 20, 15);
    print(rect.left == 3);
    rect.right = 12;
}
```

### 重写
***
```js
// JS
class B {
    say() {
        console.log(1)
    }
}

class A extends B {
    say() {
        console.log(2)
    }
}

new A().say();

// Dart
class A {
    void say() {
        print(1)
    }
}

class B extends A {
    @override
    say() {
        print(2);
    }
}
```