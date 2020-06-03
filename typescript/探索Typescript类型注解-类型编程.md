Typescript官方标准库中封装的实用工具类型。

# 实用工具类型
Typescript提供的实用工具类型用来实现常见的类型转换，这些类型工具函数是全局可见的。

`Extract`,`Exclude`,'NonNullable`

* `Extract<T, U>`: 从T中提取可以赋值给`U`的类型
* `Exclude<T, U>`: 从T中排除可以赋值给U的类型
* `NonNullable<T>`: 从T中排除null和undefined

使用示例

```js
type foo = Extract<number | string, string>;  // string
type bar = Exclude<number | string, string>; // number
type baz = NonNullable<number | string | null | undefined>;  // string | number
```

具体实现

```ts
// 主要使用条件类型 T extends U ? X : Y 实现
type Extract<T, U> = T extends U ? T : never;
type Exclude<T, U> = T extends U ? never : T;
type NonNullable<T> = T extends null | undefined ? never : T;
```

`Partial, Require, Readonly`

* Partial<T>: 将T中的所有属性设置为可选
* Require<T>: 将T中的所有属性设置为必选
* Readonly<T>: 将T中的所有属性设置为只读

具体示例

```ts
interface Type { a: number, b?: string };
let foo: Partial<Type> = { b: 'b' };
let bar: Required<Type> = { a: 1 }; // Error
let baz: Readonly<Type> = { a: 1 };
baz.a = 2; // Error
```

具体实现
ia
```ts
// 主要使用映射类型 `[K in T]: Type`及索引类型`keyof T`、`T[P]`实现
type Partial<T> = { [P in keyof T]?: T[P] };
type Require<T> = { [P in keyof T]-?: T[P] }; // 注意这里的`-?`
type Readonly<T> = { readonly [P in keyof T]: T[p]}
```

# typeof
在TS中，还可以使用typeof来获取变量的类型。

```ts
let foo: number = 3;
type bar = typeof foo; // 相当于 type bar = number;
```

# extends
前面的章节中多处使用了extends关键字。如下
原生js中类的继承

```js
class A { a: number };
class B extends A { b: string }  // B 继承 A
let a: A = new A()
let b: B = new B()
a = b
```
接口继承

```ts
interface A { a: number }
interface B extends A { b: string }
let a: A = { a: 1 };
let b: B = { b: 'b', a: 1 };
a = b; // ok ,A = B
```

泛型约束

```ts
interface A { a: number };
interface B { a: number, b: string }
type E = B extends A ? true : false;
// type E = true
```

1、从extends关键字的语义：他们之间属于继承关系，既子类继承超类。
2、从类型兼容性角度: 超类兼容子类，既子类可以赋值给超类
3、从功能上
** 类和接口中的extends用来定义，可有多个超类，中间用，分割
** 泛型约束和条件类型中的extends用来检测兼容性，即Sup是否兼容Sub

# 类型和集合
TS中的类型好比数学中的集合，类型是具有某种特定性质的JS值的集合。比如number类型对应JS中所有数值的集合。

类型集合中的分类。

* any类型对应为全集
* never类型对应为空集
* 联合类型是类型集合之间的并集
* 交叉类型是类型集合之间的交集

