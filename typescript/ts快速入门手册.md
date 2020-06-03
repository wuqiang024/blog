# ts快速入门手册
***

## 环境搭建
***
TS编写的程序不能直接通过浏览器运行，我们需要先通过TS编译器把TS代码编译成JS代码。
TS编译器是基于Node.js的，所以我们需要安装Node.js

## 安装TS编译器
通过NPM包管理工具安装TS编译器。

```js
npm i -g typescript
```

安装完成后，我们可以通过命令tsc来调用编译器.

```js
// 查看当前tsc编译器版本
tsc -v
```

## 编写代码
默认情况下，TS文件的后缀为.ts

```ts
let str: string = 'typescript';
```

## 编译执行
使用我们安装的TS编译器tsc对.ts文件进行编译

```js
tsc ./src/hello.ts
```
默认情况下会在当前文件所在目录生成同名的.js文件

## 一些有用的编译选项
***
编译命令tsc还支持许多编译选项，这里我们先来了解几个有用的。

`--outDir`: 指定编译文件输出目录

```js
tsc --outDir ./dist ./src/hello.ts
```

`target` 指定编译的代码版本目标，默认为ES3

```js
tsc --outDir ./dist --target es6 ./src/hello.ts
```

`--watch` 在监听模式下运行，当文件发生改变时自动编译

```js
tsc --outDir ./dist --target ES6 --watch ./src/hello.ts
```

通过以上几个例子，基本可以了解tsc的使用了，但是每次编译输入这么多选项是很繁琐的，好在TS提供了一个编译配置文件: `tsconfig.json`, 我们可以把上面的编译选项保存到这个配置文件中。

## 编译配置文件
***
我们可以把编译的一些选项保存在一个指定的json文件中，默认情况下tsc命令运行的时候会自动去加载所在目录下的tsconfig.json,配置文件格式如下

```js
{
    "compilerOptions": {
        "outDir": "./dist",
        "target": "ES2015",
        "watch": true
    },
    "include": ["./src/**/*"]
}
```

有了单独的配置文件，我们就可以直接运行`tsc`

## 指定加载的配置文件
***
使用 `--project`或`-p`指定配置文件目录，会默认加载该目录下的tsconfig.json文件。

```js
tsc -p ./configs
```

也可以指定某个具体的配置文件.

```js
tsc -p ./configs/ts.json
```

## 动态类型语言 & 静态类型语言
动态类型语言是在程序运行期间在做数据类型检查的语言，静态类型语言是在程序编译期间做数据类型检查的语言。

## 静态类型语言的优缺点
### 优点
* 程序编译阶段即可发现一些潜在的错误，避免程序在运行环境运行后再出现错误
* 编码规范，有利于团队合作，大型项目的开发，项目重构
* 配合IDE,编辑器提供更强大的代码智能提示/检查
* 代码既文档

### 缺点
* 麻烦
* 缺少灵活性

## 基础的简单的类型标注
### 基础类型
基础类型包括`string`,`number`,`boolean`

### 空和未定义类型
因为在Null和Undefined这两种类型有且只有一个值，在标注为`Null`和`Undefined`类型后，就表示该类型变量不能修改了。

```js
let a: null;
a = null; // ok
a = 1; // error
```

默认情况下`null`和`undefined`是所有类型的子类型。就是说你可以把null和undefined赋值给其他类型的变量。

`如果一个变量声明了但未赋值，那么该变量的值为undefined，但是如果他同时也没有标注类型的话，默认类型为any`

> 小技巧
> 因为null和undefined是其他类型的子类型，所以默认情况下会有一些隐藏的问题。

```js
let a: number;
a = null;
a.toFixed(2);
```

`指定strictNullChecks配置为true，可以有效的检测null或undefined，避免很多常见问题。`

## 对象类型
### 内置对象类型
在JS中有许多内置对象类型，比如: Object, Array, Date...，我们可以通过对象的构造函数或者类来进行标注。

```js
let a: object = {};
let arr: Array<number> = [1, 2, 3];
let d1: Date = new Date();

### 自定义对象类型
另外一种情况，很多时候，我们可能需要自定义结构的对象，这个时候，我们可以:
* 字面量标注
* 接口
* 定义类或者构造函数

> 字面量标注
```js
let a: {username: string; age: number} = {
    username: 'zMouse',
    age: 25
};
```

> 接口

```js
interface Person {
    username: string;
    age: number;
};
let a: Person = {
    username: 'zMouse',
    age: 25
};
```

接口只能作为类型标注使用，不能作为具体值，他只是一种抽象的结构定义，并不是实体，没有具体功能实现。

> 类与构造函数

```js
class Person {
    constructor(public username: string, public age: number) {

    }
}
```

功能相对强大，定义实体的同时也定义了对应的类型，但是如果只想约束某个函数接受的参数结构，没必要去定义一个类，使用接口更加简单。

## 数组类型
在TS中数组存储的类型必须一致，所以在标注数组类型的时候，同时要标注数组中存储的数据类型。

`使用泛型标注`

```js
let arr1: Array<number> = [];
arr1.push(100);
```

`简单标注`

```js
let arr2: string[] = [];
```

## 元组类型
元组类型类似数组，但是存储的元素类型不必相同，但是需要注意:
* 初始化数据的个数以及对应位置标注类型必须一致
* 越界数据必须是元组标注中的类型之一(标注越界数据可以不用对应顺序)

## 枚举类型

```js
enum HTTP_CODE {
    OK = 200,
    NOT_FOUND = 404,
    METHOD_NOT_ALLOWD
}
```

注意事项:
* key不能是数字
* value可以是数字，称为数字型枚举，也可以是字符串，称为字符串类型枚举，但不能是其他值，默认为数字0
* 枚举值可以省略，如果省略，则:
    * 第一枚举值默认为0
    * 非第一个枚举值为上一个数字枚举值+1
* 枚举值为只读(常量),初始化后不可修改

`字符串类型枚举`
枚举类型的值，也可以是字符串类型

```js
enum URLS {
    USER_REGISTER = '/user/register',
    USER_LOGIN = '/user/login'
}
```

`注意:如果前一个枚举值类型是字符串，则后续枚举项必须手动赋值`
`枚举名称可以是大写，也可以是小写，推荐使用全大写`

## 无值类型
表示没有任何数据的类型，通常用于标注无返回值函数的返回值类型，函数默认标注类型为: `void`

```js
function fn(): void {
    // 没有return或者return undefined
}
```

`在strictNullChecks为false的情况下，undefined和null都可以赋值给void，但是当strictNullChecks为true的情况下，只有undefined才可以赋值给void`

## Never类型
当一个函数永远不可能执行return的时候，返回的就是never,与void不同，void是执行了return，只是没有值，never是永远不会执行return，比如抛出错误，导致函数终止执行。

```js
function fn(): never {
    throw new Error('error');
}
```

## 任意类型
有的时候，我们并不确定这个值到底是什么类型或者不需要对该值进行类型检测，就可以标注为any类型。
* 一个变量声明未赋值，而且未标注类型的情况下，默认为any类型
* 任何类型都可以赋值给any类型
* any类型也可以赋值给任意类型
* any类型有任意属性和方法
`注:标注为any类型，也意味着放弃对该值的类型检测，同时放弃IDE的智能提示`

> 小技巧: 当指定noImplicitAny配置为true, 当函数出现隐含的any类型时报错

## 未知类型
`unknown`，3.0版本中新增，属于安全版的any,但是与any不同的是:
* unknown仅能赋值给unknown,any
* unknown没有任何属性和方法

## 函数类型

```js
function add(x: number, y: number): number {
    return x + y;
}
```

## 高级类型
### 联合类型
***
联合类型也可以成为多选类型，当我们希望标注一个变量为多个类型之一的时候，可以选择联合类型标注

```js
function css(ele: Element, attr: string, value: string | number) {
    // ...
}
```

### 交叉类型
***
交叉类型也可以称为合并类型，可以把多个类型合并到一起成为一种新的类型，以并且的关系对一个对象进行扩展。
```js
interface o1 {x: number, y: string};
interface o2 {z: number};
let o: o1 & o2 = Object.assign({}, {x:1, y:'2'}, {z: 100});
```

`小技巧: TS在编译过程中只会转换语法(比如扩展运算符，箭头函数等)，对于API是不会进行转换的(也没必要转换，而是引入一些库进行处理),如果我们的代码中使用了target中没有的API，则需要手动引入，默认情况下TS会根据target引入核心的类型库。
target为es5时: ['dom', 'es5', 'scripthost']
target为es6时: ['dom', 'es6', 'dom.iterator', 'scripthost']
如果代码中使用了这些默认载入库以外的代码，则可以通过lib选项来进行设置。`

## 字面量类型
***
有的时候，我们希望标注的不是某个类型，而是一个固定值，就可以使用字面量类型，配合联合类型更有用。

```js
function setPosition(ele: Element, direction: 'left' | 'top') {
    // ...
}
```

## 类型别名
***
有时候类型标注比较复杂，我们可以给类型取一个简单的别名。

```js
type dir = 'left' | 'top' | 'right';
function setPosition(ele: Element, direction: dir) {
    // ...
}
```

## 使用类型别名定义函数类型
***
这里需要注意一下，如果使用type来定义函数类型，和接口有点不太一样。

```js
type callback = (a: string) => string;
let fn: callback = function(a) {};

// 或者直接
let fn: (a: string) => string = function a() {};
```

## interface和type的区别
`interface`
* 只能描述 object/class/function的类型
* 同名interface自动合并，利于扩展

`type`
* 不能重名
* 能描述所有类型

## 类型推导
***
每次显式标注类型会比较麻烦，TS提供了一种更加方便的特性：类型推导。
TS会根据当前上下文自动的推导出对应的类型标注，这个过程发生在:
* 初始化变量
* 设置函数默认参数值
* 返回函数值

## 类型断言
***
有时候，我们可能标注一个更加精确的类型(缩小类型标注范围)，比如:

```js
let img = document.querySelector('#img');
```

我们可以看到img的类型为Element,而Element类型其实只是元素类型的通用类型，如果我们去访问src这个属性是有问题的，我们需要把它的类型标注得更加精确。
HTMLImageElement类型。这个时候，我们就可以使用类型断言，他类似于一种类型转换。

```typescript
let img = <HTMLImageElement>document.querySelector('#img');
let img = document.querySelector('#img') as HTMLImageElement;
```

`注意，断言只是一种预判，并不会对数据本身产生实际的作用，即:类型转换，但并非真的转换了。也就是让编译器不需要进行类型检查`

## 接口
***
接口是一种类型，不能作为值使用

`可选属性`
***
接口也可以定义可选的属性，通过?进行标注.

```typescript
interface Point {
    x: number;
    y: number;
    color?: string;
}
```

其中`color?:`表示该属性是可选的。

`只读属性`
***
我们还可以通过`readonly`来标注属性为只读

```typescript   
interface Point {
    readonly x: number;
    readonly y: number;
}
```

当我们标注了一个属性为只读，那么该属性除了初始化以外，是不能被再次赋值的。

### 任意属性
***
有的时候，我们希望给接口添加任意属性，可以通过所以类型来实现

`数字类型索引`

```typescript
interface Point {
    x: number;
    y: number;
    [prop: number]: number;
}
```

`字符串类型索引`

```typescript
interface Point {
    x: number;
    y: number;
    [prop: string]: number;
}
```

数字索引是字符串索引的子类型。

`注意: 索引签名参数类型必须为string或number之一，但两者可同时出现`

```typescript
interface Point {
    [prop1: string]: string;
    [prop2: number]: string;
}
```

`当同时存在数字类型索引和字符串类型索引的时候，数字类型的值类型必须是字符串类型的值类型或子类型`

```typescript
interface Point {
    [prop1: string]: string;
    [prop2: number]: number; // 错误
}

interface Point {
    [prop1: string]: Object;
    [prop2: number]: Date; // 正确
}
```

## 使用接口描述函数
***
我们还可以使用接口来描述一个函数

```typescript
interface IFunc {
    (a: string): string;
}
let fn: IFunc = function(a) {}
```

`注意：如果使用接口来单独描述一个函数，是没有key的`

## 接口合并
***
多个同名的接口合并成一个接口

```typescript
interface Box {
    height: number;
    width: number;
}

interface Box {
    scale: number;
}

let box: Box = {height: 5, width: 6, scale: 10};
```

* 如果合并的接口存在同名的非函数成员，则必须保证同名类型一致，否则编译报错
* 接口中的同名函数采用的是重载

## 函数的标注
*** 一个函数的标注包括
* 参数
* 返回值

```typescript
function fn(a: string): string {};
let fn: (a: string) => string = function(a) {};

type callback = (a: string): string;
interface ICallBack {
    (a: string): string;
}

let fn: callback = function(a) {};
let fn: ICallBack = function(a) {};
```

## 可选参数和默认参数
***
通过参数后面添加? 来标注该参数是可选的

```typescript
function css(ele: HTMLElement, attr: string, val?: any) {}
```

## 默认参数
***
我们还可以给参数设置默认值
* 有默认值的参数也是可选的
* 设置了默认值的参数可以根据值自动推导类型

```typescript
function sort(item: Array<number>, order = 'desc') {}
sort([1, 2, 3]);

// 也可以通过联合类型来限制取值
function sort(items: Array<number>, order: 'desc'|'asc' = 'desc') {}

// ok
sort([1, 2, 3]);
```

## 剩余参数
***
剩余参数是一个数组，所以标注的时候一定要注意

```typescript
interface IObj {
    [key: string]: any;
}

function merge(target: IObj, ...others: Array<IObj>) {}
```

## 函数中的this
***
无论是JS还是TS，函数中的this都是我们需要关心的，那函数中this的类型该如何进行标注呢？
* 普通函数
* 箭头函数

### 普通函数
对于普通函数而言，this是会随着函数调用环境的变化而变化的，所以默认情况下，普通函数中的this被标注为any,但我们可以在函数的第一个参数位(他不占据实际参数的位置)上显式的标注this的类型。

```typescript
interface T {
    a: number;
    fn: (x: number) => void;
}

let obj1: T = {
    a: 1,
    fn(x: number) {
        console.log(this) // any类型
    }
};

let obj2: T = {
    a: 1,
    fn(this: T, x: number) {
        console.log(this); // 通过第一个参数位标注this的类型，他对实际参数不会有影响。
    }
}
```

### 箭头函数
箭头函数的this不能像普通函数那样进行标注，他的this标注类型取决于他所在的作用域this的标注类型。

```typescript
interface T {
    a: number;
    fn: (x: number) => void;
}

let obj2: T = {
    a: 2,
    fn(this: T) {
        return () => {
            console.log(this); // T
        }
    }
```

## 函数重载
***
有的时候，同一个函数会接收不同类型的参数，返回不同类型的返回值，我们可以使用函数重载来实现。

```typescript
function showOrHide(ele: HTMLElement, attr: 'display', value: 'block' | 'none') {
    // ...
}
function showOrHide(ele: HTMLElement, attr: 'opacity', value: number) {}
function showOrHide(ele: HTMLElement, attr: string, value: any) {
    ele.style[attr] = value;
}
```

## class 类
通过class定义了一个类以后，我们可以通过new关键字来调用该类从而得到该类型的一个具体对象。也就是实例化
为什么类可以像函数一样去调用呢，其实我们执行的不是这个类，而是类中包含的一个特殊函数: 构造函数 => constructor

```typescript
class User {
    constructor() {
        console.log('实例化');
    }
}
let user1 = new User;
```

* 默认情况下，构造函数是一个空函数
* 构造函数会在类被实例化的时候调用
* 我们定义的构造函数会覆盖默认的构造函数
* 如果在实例化(new)一个类的时候无需传入参数，则可以省略()
* 构造函数constructor不允许有return和返回值类型标注的(因为要返回实例对象)，通常情况下，我们会把一个类实例化的时候初始化相关代码写在构造函数中，比如对类成员属性的初始化赋值。

## 成员属性与方法定义

```typescript
class User {
    id: number;
    username: string;
    constructor(id: number, username: string) {
        this.id = id;
        this.username = username;
    }
    postArticle(title: string, content: string): void {
        console.log(`${title}`);
    }
}
```

### this关键字
***
在类内部，我们可以通过this关键字来访问类的属性和方法。

### 构造函数参数属性
***
因为在构造函数中对类成员属性进行传参赋值初始化是一个比较常见的场景，所以ts提供了一个简化操作：给构造函数参数添加修饰符来直接生成成员属性。

* public就是类的默认修饰符，表示该成员可以在任何地方进行读写操作。

```typescript
class User {
    constructor(public id: number, public username: string) {}
    postArticle(title: string, content: string): void {
    }
}
```

### 继承
***
在ts中，也是通过extends关键字来实现类的继承。

```typescript
class VIP extends User {}
```

### super关键字
在子类中，我们可以通过super来引用父类
* 如果子类没有重写构造函数，则会在默认的constructor中调用super()
* 如果子类有自己的构造函数，则需要在子类构造函数中显式的调用父类构造函数:super(参数)，否则会报错
* 在子类构造函数中只有调用了父类构造函数之后才可以使用this
* 在子类中，可以通过super来访问父类的成员属性和方法
* 通过super访问父类的同时，会自动绑定上下文对象为当前子类this

### 方法的重写和重载
默认情况下，子类成员方法继承自父类，但是子类也可以对他们进行重写和重载

## 修饰符
***
有的时候，我们希望对类成员(属性，方法)进行一定的访问控制，来保证数据的安全，通过类修饰符可以做到这一点，目前TS提供了四种修饰符。
* public
* protected
* private
* readonly

`public`修饰符
这个是类成员的默认修饰符，他的访问级别为:
* 自身
* 子类
* 类外

`protected`修饰符
他的访问级别为
* 自身
* 子类

`private`修饰符
他的访问级别为
* 自身

`readonly`修饰符
只读修饰符只能针对成员属性使用，而且必须在声明时或构造函数里被初始化，他的访问级别为:
* 自身
* 子类
* 类外

### 寄存器
***
有的时候，我们需要对类成员属性进行更加细腻的控制，就可以使用寄存器来完成这个需求，通过寄存器，我们可以对类成员属性的访问进行拦截并加以控制，更好的控制成员属性的设置和访问边界，寄存器分为两种。
* getter
* setter

`getter`
访问控制器，当访问指定成员属性时使用

`setter`
设置控制器，当设置指定成员属性时调用

### 静态成员
***
前面我们说到的是成员属性和方法都是实例对象的，但是有的时候，我们需要给类本身添加成员，区分某成员是静态还是实例的。
* 类的静态成员是属于类的，所以不能通过实例对象(包括this)来进行访问，而是直接通过类名访问(不管是类内还是类外)
* 静态成员也可以通过访问修饰符修饰
* 静态成员属性一般约定全大写。

## 抽象类
***
有的时候，一个基类(父类)的一些方法无法确定具体的行为，而是由继承的子类去实现。

### abstract关键字
***
如果一个方法没有具体的实现方法，则可以通过abstract关键字进行修饰

```typescript
abstract class Component<T1, T2> {
    public state: T2;
    constructor(public props: T1) {}
    public abstract render(): string;
}
```

使用抽象类有一个好处:
约定了所有继承子类的所必须实现的方法，使类的设计更加的规范。

`使用注意事项`:
* abstract修饰的方法不能有方法体
* 如果一个类有抽象方法，那么该类也必须是抽象的
* 如果一个类是抽象的，那么就不能使用new进行实例化(因为抽象类表明该类有未实现的方法，所以不允许实例化)
* 如果一个子类继承了一个抽象类，那么该子类就必须实现抽象类中所有的抽象方法，否则该类还得声明为抽象的。

## 类与接口
***
在前面我们已经学习了接口的使用，通过接口，我们可以为对象定义一种结构和契约。我们还可以把接口跟类进行结合，通过接口，让类去强制符合某种契约，从某个方面说，当一个抽象类中只有抽象的时候，他就跟接口区别不大了，这个时候，我们更推荐通过接口的方式来定义契约。
* 抽象类编译后还是会产生实体代码，接口不会
* TS只支持单继承，即一个子类只能有一个父类，但是一个类可以有多个接口。
* 接口不能实现，抽象类可以

### implements
***
在一个类中使用接口并不是使用extends关键字，而是implements
* 与接口类似，如果一个类implements了一个接口，那么就必须实现该接口定义的契约
* 多个接口用逗号分隔
* implements与extends可以同时存在
* 接口也可以继承

```typescript
interface ILog {
    getInfo(): string;
}
interface IStorage extends ILog {
    save(data: string): void;
}
```

## 类与对象类型
***
当我们在TS定义一个类的时候，其实同时定义了两个不同的类型
* 类类型(构造函数类型)
* 对象类型

首先，对象类型好理解，就是我们new出来的实例类型。
那类类型是什么，我们知道JS中的类，或者说是TS中的类其实本质上还是一个函数，当然我们也称之为构造函数，那么这个类或者构造函数本身也是有类型的，那么这个类型就是类的类型。

```typescript
class Person {
    static type = '人“；
    name: string;
    age: number;
    gender: string;
    // 类的构造函数也是属于类的
    constructor(name: string, age: number, gender: '男' | '女' = '男') {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }
    public eat(): void {
        // ...
    }
}

let p1 = new Person('zMouse', 35, '男');
p1.eat();
Person.type;
```

上面的例子中，有两个不同的数据
* Person类(构造函数)
* 通过Person实例化出来的对象p1

对应的也有两种不同的类型
* 实例的类型(Person)
* 构造函数的类型(typeof Person)

用接口的方式描述如下

```typescript
interface Person {
    name: string;
    age: number;
    gender: string;
    eat(): void;
}

interface PersonConstructor {
    // new 表示他是一个构造函数
    new (name: string, age: number, gender: '男' | '女'): PersonInstance;
    type: string;
}
```

在使用的时候格外注意

```typescript
function fn1(arg: Person /* 如果希望这里传入的Person的实例对象 */) {
    arg.eat()
}

fn1(new Person('', 1, '男'));

function fn2(arg: typeof Person /* 如果希望传入的Person构造函数 */) {
    new arg('', 1, '男');
}
fn2(Person);
```

## TS的模块系统
***
### 模块
无论是JS还是TS都是以一个文件作为模块最小单元
* 任何一个包含了顶级import或export的文件都被当做是一个模块
* 相反的一个文件如果不带有顶级的import或export，那么他的内容就是全局可见的。

### 模块编译
TS编译器能够根据相应的编译参数，把代码编译成指定的模块系统使用的代码
`module`选项
在TS编译选项中，module选项是用来指定生成哪个模块系统的代码，看设置的值有: 'none', 'commonjs', 'udm', 'amd', 'es6'/'es2015/esnext', 'System'

* target = 'es3' 或 'es5': 默认使用commonjs
* 其他情况，默认es6

### 模块导出默认值的问题
如果一个模块没有默认导出

```typescript
export let obj = {};
```

则在引入该模块的时候，需要使用下列一些方法来导入

```typescript
import v from './m1' // error,没有默认导出

import { obj } from './m1';
import * as m1 from './m1';
```

### 加载非TS文件
有的时候，我们需要引入一些js的模块，比如导入一些第三方的使用js而非ts编写的模块，默认情况下tsc是不对非ts模块文件进行处理的。
我们可以通过allowJs选项开启该特性。

```typescript
// m1.js
export default 100;
// main.ts
import m1 from './m1.js'
```

### 非ESM模块中的默认值问题
在ESM模块中可以设置导出默认值

```typescript
export default 'hello';
```

但是在commonjs, amd中是没有默认值设置的，他们导出的是一个对象(exports);

```js
module.exports = {}
```

在TS中导入这种模块的时候会出现`模块没有默认导出的错误提示`。

简单的一些做法:

```typescript
import * as m from './m1.js'
```

通过配置选项解决:
`allowSyntheticDefaultImports`设置为true，允许从没有设置默认导出的模块默认导入。

虽然通过上面的方式可以解决编译过程中的检测问题，但是编译后的具体要运行代码还是有问题的。

`esModuleInterop`设置为true，则在编译的同时生成一个__importDefault函数，用来处理具体的default默认导出。

`注意:以上设置只能当module不为es6+的情况下有效`

### 以模块的方式加载JSON文件
***
TS2.9+版本添加了一个新的编译选项： resolveJsonModule，他允许我们把一个Json文件作为模块进行加载。
`resolveJsonModule`设置为true，可以把json文件作为一个模块进行解析。

```typescript
// data.json
{
    "name": "zMouse"
}
// ts文件
import * as userData from './data.json';
console.log(userData.name)
```

## 命名空间
在TS中，export和import称为外部模块，TS还支持一种内部模块`namespace`，他的主要作用只是单纯的在文件内部隔离作用域。

```typescript
namespace k1 {
    let a = 10;
    export var obj = {
        a
    }
}

namespace k2 {
    let a = 20;
    console.log(k1.obj);
}
```

## 模块解析策略
### 什么是模块解析
模块解析是指编译器在查找导入模块内容时所遵循的流程。

### 相对和非相对模块导入
根据模块引用是相对的还是非相对的，模块导入会以不同的方式解析。

### 相对导入
相对导入以/, ./ 或../开头的引用

### 模块解析策略
为了兼容两种不同的模块系统(CommonJS, ESM),TS支持两种不同的模块解析策略，Node，Classic,当--module选项为AMD,System,ES2015时，默认为Classic，其他情况为Node

`--moduleResolution`选项
除了根据--module选项自动选择默认模块系统类型，我们还可以通过`--moduleResolution`选项来手动指定解析策略。

```json
{
    "moduleResolution": "node"
}
```

### Classic模块解析策略
该策略是TS以前的默认解析策略，他已经被新的Node策略所取代，现在使用该策略主要是为了向后兼容。

相对导入:
```js
// /src/m1/a.ts
import b from './b.ts';
```
解析查找流程: src/m1/b.ts

默认后缀补全
```js
import b from './b';
```
解析查找流程:
1、/src/m1/b.ts
2、/src/m1/b.d.ts

非相对导入:
```js
// /src/m1/a.ts
import b from 'b';
```
对于非相对导入，则会从包含导入文件的目录开始依次向上级目录遍历查找，直到根目录为止。
1、/src/m1/b.ts
2、/src/m1/b.d.ts
3、/src/b.ts
4、/src/b.d.ts
5、/b.ts
6、/b.d.ts

### Node模块解析策略
该策略是参照了node.js的模块解析机制

相对导入
```js
import b from './b'
```
在Classic中，模块只会按照单个的文件进行查找，但是在node.js中，会首先按照单个文件进行查找，如果不存在，则会按目录进行查找。
1、/src/m1/b.ts
2、/src/m1/b/package.json中'main'中指定的文件
3、/src/m1/b/index.js

非相对导入
```js
import b from 'b';
```
对于非相对导入模块，解析是很特殊的，node.js会在一个特殊文件夹node_modules里查找，并且在查找过程中从当前目录的node_modules目录下逐级向上级文件夹中进行查找。
1、/src/m1/node_modules/b.js
2、/src/m1/node_modules/b/package.json中'main'中指定的文件
3、/src/m1/node_modules/b/index.js
4、/src/node_modules/b.js
5、/src/node_modules/b/package.json中main中指定的文件
6、/src/node_modules/b/index.js

现在TS使用了与node.js类似的模块解析策略，但是TS增加了其他几个源文件扩展名的查找(.ts, .tsx, .d.ts)，同时TS在package.json里使用字段types来表示main的意义。

## 装饰器
### 什么是装饰器
装饰器-Decorators在TS中是一种可以在不修改类代码的基础上通过添加标注的方式来对类型进行扩展的一种方式
* 减少代码量
* 提高代码扩展性，可读性和可维护性

### 装饰器语法
装饰器的使用极其简单
* 装饰器本质上就是一个函数
* 通过特定语法在特定位置调用装饰器函数即可对数据进行扩展

### 启用装饰器特性
* experimentalDecorators: true

### 装饰器
装饰器是一个函数，他可以通过`@装饰器函数`这种特殊的语法附加在类，方法，访问符，属性，参数上，对他们进行包装，然后返回一个包装后的目标对象。装饰器工作在类的构建阶段，而不是使用阶段。

```js
function 装饰器1() {}

@装饰器1
class MyClass {
    @装饰器2
    a: number;

    @装饰器3
    static property: number;
}
```

### 类装饰器
* 应用于类的构造函数
* 第一个参数(也只有一个参数) 类的构造函数作为其唯一的参数

### 方法装饰器
* 作用于类的方法上
* 第一个参数(静态方法: 类的构造函数，实例方法: 类的原型对象)
* 第二个参数(方法名称)
* 第三个参数(方法描述符对象)

### 属性装饰器
* 作用于类的属性上
* 第一个参数(静态方法: 类的构造函数，实例方法: 类的原型对象)
* 第二个参数(属性名称)

### 访问器装饰器
* 应用于类的访问器上
* 第一个参数(同上)
* 第二个参数(属性名称)
* 第三个参数(方法描述符对象)

### 参数装饰器
* 应用在参数上
* 第一个参数(同上)
* 第二个参数(方法名称)
* 第三个参数(参数在函数参数列表中的索引)

### 装饰器执行顺序
实例装饰器
属性 => 访问符 => 参数 => 方法
静态装饰器
属性 => 访问符 => 参数 => 方法
类
类

## 元数据
***
在装饰器函数中，我们可以拿到类，方法，访问符，属性，参数的基本信息，但是我们想要获得更多信息就要通过另外的方式来进行：元数据

### 什么是元数据
元数据是用来描述数据的数据，在我们的程序中，对象，类等都是数据，他们描述了某种数据，另外还有一种数据，他们可以用来描述对象，类，这些用来描述数据的数据就是元数据。

`比如歌曲本身就是一组数据，同时还有一组用来描述歌手，格式，时长的数据，那么这组数据就是歌曲数据的元数据。

### 使用reflect-metadata
首先需要安装`reflect-metadata`

```js
npm install reflect-metadata
```

我们可以给类，方法定义元数据。

* 元数据会被附加在指定的类，方法等数据上，但是又不会影响类，方法本身的代码
* 设置`Reflect.difineMetadata(metadataKey,metadataValue,target,propertyKey)`
* metadataKey: meta数据的key
* metadataValue: meta数据的value
* target: meta数据附加的目标
* propertyKey: 对应的property key

调用方式
* 通过Reflect.defineMetadata方式调用来添加元数据
* 通过@Reflect.metadata装饰器来添加元数据

```js
import 'reflect-metadata';

@Reflect.metadata('n', 1)
class A {
    @Reflect.metadata('n', 2)
    public static method1() {}
}

// 或者
Reflect.defineMetadata('n', 1, A);
Reflect.defineMetadata('n', 1, A, 'method1')

Reflect.getMetadata('n', A);
```

获取元数据是
`Reflect.getMetadata(metadataKey, target, propertyKey)`
