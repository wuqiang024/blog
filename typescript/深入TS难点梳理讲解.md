# TS站点
* Typescript中文网
* 深入理解Typescript
* Typescript handbook
* TypeScript 精通指南

# 可索引类型
***
可索引类型也是接口的一种表现形式，非常实用!

```typescript
interface StringArray {
    [index: number]: string;
}

let myArray: StringArray;
myArray = ['bob', 'fred'];

let myStr: string = myArray[0];
```

上面的例子里，我们定义了StringArray接口，他具有索引签名。这个索引签名表示了当用number去索引StringArray时会得到string类型的返回值。TS支持两种索引签名: `数字`和`字符串`。可以同时使用两种类型的索引，`但是数字索引的返回值必须是字符串索引返回值类型的子类型。`

这是因为当使用number来索引时，JS会将他转换成string然后再去索引对象。也就是说用100(一个number)去索引等于使用'100'(一个string)去索引，因此两者需要保持一致。

```typescript
class Animal {
    name: string;
}

class Dog extends Animal {
    breed: string;
}

// 错误，使用数值型的字符串索引，有时会得到完全不同的Animal
interface NotOkay {
    [x: number]: Animal;
    [y: string]: Dog;
}
```

下面的例子里，name的类型与字符串索引类型不匹配，所以类型检查器给出一个错误提示:

```typescript
interface NumberDictionary {
    [index: string]: number;
    length: number; // 可以，length是number类型
    name: string; // 错误,'name'的类型与索引类型返回值的类型不匹配
}
```

当然，我们也可以将索引签名设置为只读，这样就可以防止给索引赋值

```typescript
interface ReadonlyStringArray {
    readonly [index: number]: string;
}
let myArray: ReadonlyStringArray = ['alice', 'bob'];

myArray[2] = 'mally'; // error;
```

# interface和type关键字
***
interface和type两个关键字的含义和功能都非常的接近。这里我们罗列下主要的区别。

`interface`
* 同名的interface自动聚合，也可以跟同名的class自动聚合
* 只能表示class, object, function类型

`type`
* 不仅仅能够表示object, class, function
* 不能重名(自存不存在同名聚合了)，扩展已有的type需要创建新type
* 支持复杂的类型操作

举例说明下上面罗列的几点:

## Objects/Functions
***
都可以用来表示Object和Function，只是语法上有所不同而已

```typescript
interface Point {
    x: number;
    y: number;
}

interface SetPoint {
    (x: number, y: number): void;
}
```

```typescript
type Point = {
    x: number;
    y: number;
}

type SetPoint = (x: number, y: number) => void;
```

## 其他数据类型
***
与interface不同，type还可以用来标书其他的类型，比如基本数据类型，元素，并集等

```typescript
type name = string;
type PartialPointX = { x: number };
type PartialPoint = PartialX | PartialY;
type Data = [number, string, boolean];
```

## Extend
***
都可以被继承，但是语法上会有些不同。另外需要注意的是， `interface`和`type`彼此并不互斥。

## interface extends interface

```typescript
interface PartialPointX { x: number };
interface PartialPoint extends PartialPointX { y: number };
```

## type extends type

```typescript
type PartialPointX = { x: number };
type Point = PartialPointX & { y: number };
```

## interface extends type

```typescript
type PartialPointX = { x: number };
interface Point extends PartialPointx { y: number };
```

## type extends interface

```typescript
interface PartialPointX = { x: number };
type Point = PartialPointX & { y: number };
```

## implements
一个类，可以以完全相同的形式去实现interface或者type，但是类和接口都被视为静态蓝图(static blueprint)，因此，他们不能实现/继承 联合类型的type.

```typescript
interface Point {
    x: number;
    y: number;
}

class SomePoint implements Point {
    x: 1;
    y: 2;
}

type Point2 = {
    x: number;
    y: number;
}

class SomePoint2 implements Point2 {
    x: 1;
    y: 2;
}

type PartialPoint = { x: number } | { y: number };
// error; cant implements a union type
class SomePartialPoint implements PartialPoint {
    x: 1;
    y: 2;
}
```

## 声明合并
与type不同，interface可以被重复定义，并且会被自动聚合

```typescript
interface Point { x: number };
interface Point { y: number };

const point: Point = { x: 1, y: 2 };
```

## only interface can
在实际开发中，有的时候也会遇到interface能够表达，但是type做不到的事情，`给函数挂载属性`

```typescript
interface FuncWithAttachment {
    (param: string): boolean;
    someProperty: number;
}

const testFunc: FuncWithAttachment = function(param: string) {
    return param.indexOf('Neal') > -1;
};

const result = testFunc('test');  // 有类型提醒
testFunc.someProperty = 4;
```

## & 和 | 操作符
这里我们需要区分，| 和 & 并非位运算符。我们可以理解为&表示必须同时满足所有的契约。 | 表示可以只满足一个契约。

```typescript
interface IA {
    a: string;
    b: string;
}

type IB {
    b: number;
    c: number[];
}

type IC = IA | IB; // IC的key，包含ab或者bc即可，当然，包含abc也可以
type ID = IA & IB; // ID的key必须包含abc
```

## 交叉类型
交叉类型，我们可以理解为合并，其实就是将多个类型合并为一个类型。

`Man & WoMan`
* 同时是Man和WoMan
* 同时拥有Man和Woman这两种类型的成员

```typescript
interface ObjectConstructor {
    assing<T, U>(target: T, source: U): T & U;
}
```

以上是TS的源码实现，下面我们再看一个我们日常生活使用的例子

```typescript
interface A {
    name: string;
    age: number;
    sayName: (name: string) => void;
}

interface B {
    name: string;
    gender: string;
    sayGender: (gender: string) => void;
}

let a: A & B;

// 这是合法的
a.age;
a.sayGender
```

`注意: T & never = never`

## extends
extends即为扩展，继承，在ts中，extends关键字既可以来扩展已有的类型，也可以对类型进行限定。在扩展已有类型时，不可以进行类型冲突的覆盖操作。例如，其类型中键a为string,在扩展出的类型中无法将其改为number。

```typescript
type num = {
    num： number;
}

interface IStrNum extends num {
    str: string;
}

// 与上面等价
type TStrNum = A & {
    str: string
}
```

在TS中，我们还可以通过条件类型进行一些三目操作：T extends U ? X : Y;

```typescript
type IsEqualType<A, B> = A extends B ? (B extends A ? true : false) : false;
type NumberEqualsToString = IsEqualType<number, string>; // false
type NumberEqualsToNumber = IsEqualType<number, number>; // true;
```

## keyof
`keyof是索引操作符`，用于获取一个常量的类型，这里的常量是指任何可以在编译期间确定的东西，例如const, function, class等，他是从实际运行代码通向类型系统的单行道。理论上，任何运行时的符号名想要为类型系统所用，都要加上typeof。

在使用class时，class名表示实例类型，typeof class表示class本身类型。是的，这个关键字和js的typeof关键字重名了。

假设T是一个类型，那么keyof T产生的类型就是T的属性名称字符串字面量类型构成的联合类型。

`注意，上述的T是数据类型，并非数据本身`

```typescript
interface IQZQD {
    cnName: string;
    age: number;
    author: string;
}
type ant = keyof IQZQD;
```

在vscode上，我们可以看出ts推断出来的ant;
type ant = 'cnName' | 'age' | 'author';
注意，如果T是带有字符串索引的类型，那么keyof T是string或number类型。

# 泛型
泛型可以应用于function，interface, type或class中，但是注意，`泛型不能应用于类的静态成员`
几个简单的例子.

```typescript
function log<T>(value: T): T {
    return value;
}

// 两种调用方式
log<string[]>(['a', 'b']);
log(['a', 'b']);
log('test');
```

`泛型类型，泛型接口`

```typescript
type Log = <T>(value: T) => T;
let myLog: Log = log;

interface Log<T> {
    (value: T): T
}

let myLog: Log<number> = log; // 泛型约束了整个接口，实现的时候必须制定类型，如果不指定类型，就在定义的之后指定一个默认的类型。myLog(1);
```

我们也可以把泛型变量理解为函数的参数，只不过是另一个维度的参数，是代表类型而不是代表值的参数。

```typescript
class Log<T> {
    run(value: T) {
        console.log(value);
        return value;
    }
}

let log1 = new Log<number>()  // 实例化的时候可以显示传入泛型的类型
log1.run(1);
let log2 = new Log();
log2.run({a: 1}) // 也可以不传入类型参数，当不指定的时候，value的值就可以是任意的值
```

`类型约束,需预定义一个接口`

```typescript
interface Length {
    length: number;
}
function logAdvance<T extends Length>(value: T): T {
    console.log(value, value.length);
    return value;
}

// 输入的参数不管是什么类型，都必须有length属性
logAdvance([1]);
logAdvance('123');
logAdvance({length: 3});
```

泛型的好处:
* 函数和类可以轻松的支持多种类型，增强程序的扩展性
* 不必写多条函数重载，冗长的联合类型声明，增强代码的可读性
* 灵活控制类型之间的约束

## 小试牛刀

```typescript
function pluck<T, K extends keyof T>(o: T, name: K[]): T[K][] {
    return names.map(n => o[n]);
}

interface Person {
    name: string;
    age: numer;
}

let person: Person = {
    name: 'Jarid',
    age: 35
};

let strings: string[] = pluck(person, ['name', 'name', 'name']);
// ['Jarid', 'Jarid', 'Jarid']
```

分析下Pluck方法的意思
* <T, K extends of T> 约束了这是一个泛型函数
* keyof T 就是提取T中的所有的常量key，即为: "name" | "age"
* K extends keyof Person 即为K是"name" or "age"
* 结合以上泛型解释，再看形参
* K[]即为只能包含"name"or"age"的数组
* 再看返回值
* T[K][]后面的[]是数组的意思，而T[K]就是去对象的T下的key: K的value

# 工具泛型
## Partial
Partial的作用就是将传入的属性变为可选。
由于keyof关键字已经介绍了，其实就是用来取得一个对象接口的所有key值。在介绍Partial之前，我们再介绍下in操作符。

```typescript
type Keys = 'a' | 'b';
type Obj = {
    [p in Keys]: any;
} // -> { a: any, b: any }
```

然后再看Partial的实现:

```typescript
type Partial<T> = { [P in keyof T] ?: T[P] };
```

翻译一下就是keyof T拿到T的所有属性名，然后in进行遍历，将值赋给P，最后T[P]取得相应的属性值，然后配合?:改为可选。

## Required
Required的作用是将传入的属性变为必选项。

```typescript
type Required<T> = { [P in keyof T] -?: T[P] };
```

## Readonly
将传入的属性变为只读香:

```typescript
type Readonly<T> = { readonly [P in keyof T]: T[P] };
```

## Record
该类型可以将K中所有属性的值转为T类型。

```typescript
type Record<K extends keyof any, T> = {
    [P in k]: T;
}
```

可以根据K中的所有可能值来设置key，以及value的类型，举个例子

```typescript
type T11 = Record<'a' | 'b' | 'c', Person>; // -> { a: Person; b: Person; c: Person }
```

## Pick
从T中取出一系列K的属性

```typescript
type Pick<T, K extends keyof T> = {
    [P in K]: T[P]
}
```

## Exclude
Exclude将某个类型中属于另一类的类型移除掉

```typescript
type Exclude<T, U> = T extends U ? never : T;
```

以上语句的意思是，如果T能赋值给U类型的话，那么就会返回never类型，否则返回T，最终结果是将T中的某些属于U的类型移除掉.

```typescript
type T00 = Exclude<'a' | 'b' | 'c' | 'd', 'a' | 'b' | 'f'>;
// => 'c' | 'd'
```

可以看到T是'a'|'b'|'c'|'d',然后U是'a'|'c'|'f'，返回的新类型就可以将U中的类型移除掉，也就是'b'|'d'了；

## Extract
Extract的作用是提取出T包含在U中的元素，换种更加贴近语义的说法就是从T中提取出U，源码如下:

```typescript
type Extract<T, U> = T extends U ? T : never;
```

Demo

```typescript
type T01 = Extract<'a' | 'b' | 'c' | 'd', 'a' | 'c' | 'f'>; // => 'a' | 'c'
```

## Omit
Pick和Exclude进行组合，实现忽略对象某些属性功能，源码如下:

```typescript
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
```

Demo

```typescript
type Foo = Omit<{name: string, age: number}, 'name'> // => { age: number };
```

# 类型断言
断言这种东西还是少用，对于初学者，估计最快熟练掌握的就是断言了。毕竟any大法好。
TS允许我们覆盖他的推断，然后根据我们自定义的类型取分析他，这种机制，我们称为类型断言。

```typescript
const nealyang = {};
nealyang.enName = 'test1'; // error, 'enName'属性不存在于'{}'
```

```typescript
interface INealyang = {
    enName: string;
    cnName: string;
}

const nealyang = {} as INealyang; // const nealyang = <INealyang> {};
nealyang.enName = 'test';
```

类型机制比较简单，其实就是纠正ts对类型的判断，当然，是不是纠正就看你自己的了。
需要注意以下两点即可：

* 推荐类型断言的语法使用as 关键字，而不是<>，防止歧义
* 类型断言并非是类型转换，类型断言发生在编译阶段，类型转换发生在运行时。
