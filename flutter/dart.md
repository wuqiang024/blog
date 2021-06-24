# 词法闭包
`闭包即一个函数对象，即使函数对象的调用在它原始作用域之外，依然能够访问它词法作用域内的变量。`

# 返回值
所有函数都会返回一个值。如果没有明确指定返回值，函数体会隐式的添加return null；语句

# 要注意的运算符
`~/`: 整除
`%`: 求余
`??`: if null
`..`: cascade

# 类型判定运算符
as, is 和 is!运算符用于在运行时处理类型检查
`as` Typecast
`is` True if object has the specified type
`is!` False if the object has the specified type

# 赋值运算符
使用 = 为变量赋值。使用`??=`运算符时，只有当被赋值的变量为null时才会赋值给他。
```js
a = value;
b ??= value; // 如果b为空时，将变量赋值给b，否则b的值保持不变。
```

## 条件表达式
```js
expr1 ?? expr2 
// 如果expr1是non-null，返回expr1的值，否则执行并返回expr2
```

# 获取对象的类型
使用对象的runtimeType属性，可以在运行时获取对象的类型，runtimeType返回一个Type对象。

# 默认构造函数
在没有声明构造函数的情况下，Dart会提供一个默认的构造函数。默认构造函数没有参数并会调用父类的无参构造函数。

# 构造函数不被继承
子类不会继承父类的构造函数，子类不声明构造函数，那么他就只有默认构造函数(匿名，没有参数)

# 命名构造函数
使用命名构造函数可以为一个类实现多个构造函数，也可以使用命名构造函数来更清晰的表明函数意图

```js
class Point {
    num x, y;
    Point(this.x, this.y);
    // 命名构造函数
    Point.origin() {
        x = 0;
        y = 0;
    }
}
```

切记，构造函数不能够被继承，这意味着父类的命名构造函数不会被子类继承。如果希望使用父类中定义的命名构造函数创建子类，就必须在子类中实现该函数。

# 调用父类非默认构造函数
默认情况下，子类的构造函数会自动调用父类的默认构造函数(匿名，无参数)。父类的构造函数在子类构造函数体开始执行的位置被调用。如果提供航了一个初始化参数列表，则初始化参数列表在父类构造函数执行之前执行。总之，执行顺序如下
* 初始化参数列表
* 父类的无名构造函数
* 主类的无名构造函数

如果父类中没有匿名无参的构造函数，则需要手工调用父类的其他构造函数。在当前构造函数冒号之后，函数体之前。声明调用父类构造函数。
```js
class Person {
    String firstName;
    Person.fromJson(Map data) {
        print('in Person')
    }
}

class Employee extends Person {
    Employee.fromJson(Map data) : super.fromJson(data) {
        print('in employee');
    }
}
```

# 初始化列表
除了调用超类构造函数之外，还可以在构造函数执行体之前初始化实例变量。各参数的初始化用逗号分隔。
```js
Point.fromJson(Map<String, num> json): x = json['x'], y = json['y'] {
    print('In Point.fromJson(): ($x, $y)');
}
```

用初始化列表可以很方便的设置final字段。
```js
import 'dart:math';

class Point {
    final num x;
    final num y;
    final num distanceFromOrigin;

    Point(x, y): x = x, y = y, distanceFromOrigin = sqrt(x * x + y * y);
}

main() {
    var p = new Point(2, 3);
    print(p.distanceFromOrigin);
}
```

# 重定向构造函数
有时候构造函数的唯一目的是重定向到同一个类中的另一个构造函数。重定向构造函数的函数体为空，构造函数的调用在冒号之后。
```js
class Point {
    num x, y;
    Point(this.x, this.y);
    Point.alongXAxis(num x) : this(x, 0);
}
```

# 元数据
使用元数据可以提供有关代码的其他信息。元数据注释以字符@开头，后跟对编译时常量(如deprecated)的引用或对常量构造函数的调用。
对于所有Dart代码有俩种可用注解: `@deprecated`和`@override`。
```js
class Television {
    @deprecated
    void activate() {
        turnOn();
    }

    void turnOn() {}
}
```

# typedef 为函数起一个别名
`typedef Compare = int Function(Object a, Object b);`
目前只能为函数起别名


# 可调用类
通过实现类的call()方法，能够让类像函数一样被调用。
```js
class WannabeFunction {
    call(String a, String b, String c) => '$a $b $c';
}

main() {
    var wf = new WannabeFunction();
    var out = wf('hi', 'there', 'gang');
}
```

# 生成器
当你需要延迟生成一系列值时，可以考虑用生成器函数。 Dart内置支持两种生成器函数。
* Synchronous生成器: 返回一个Iterable对象
* Asynchronuous生成器: 返回一个Stream对象

通过在函数体前标记 sync*，可以实现一个同步生成器，使用yield语句来传递值。

```js
Iterable<int> natural(int n) sync* {
    int k = 0;
    while(k < n) yield k++;
}
```

通过在函数体标记async*，可以实现一个异步生成函数，使用yield来传递值。

```js
Stream<int> asynchronous(int n) async* {
    int k = 0;
    while(k < n) yield k++;
}
```