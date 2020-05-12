# TS一些工具泛型的使用及实现
***

## Partial
Partial作用是将传入的属性变为可选项。
首先我们要理解两个关键字`keyof`和`in`，keyof可以用来取得一个对象接口的所有key值。
比如

```js
interface Foo {
    name: string;
    age: number
}
type T = keyof Foo // => 'name' | 'age'
```

而in则可以遍历枚举类型，例如

```js
type keys = 'a' | 'b';
type obj = {
    [p in keys]: any
} // => { a: any, b: any }
```

keyof 产生联合类型，in则可遍历枚举类型，所以他们经常一起使用，看下Partial源码

```js
type Partial<T> = { [P in keyof T]?: T[P] };
```

上面语句的意思是`keyof T`拿到T所有属性名，然后in进行遍历，将值赋给P，最后T[P]取得相应属性的值，结合中间的？我们就明白了Partial的含义了。

## Required
Required是将传入的属性变为必选项，源码如下
`type Required<T> = { [P in keyof T]-?: T[P] }`
我们发现一个有意思的用法`-?`，这里很好理解就是将可选项代表的`?`去掉，从而让这个类型变成必选项，与之对应的还有个`+?`，这个含义自然与`-?`之前相反，他是用来把属性变成可选项的。

## Mutable(未包含)
类似地，其实还有对`+`和`-`，这里要说的不是变量之间的进行加减而是对`reaeonly`进行加减。
以下代码的作用就是将T的所有属性的readonly移除，你也可以写一个相反的出来。

```js
type Mutable<T> = {
    -readonly [P in keyof T]: T[P]
}
```

## Readonly
将传入的属性变为只读选项，源码如下

```js
type Readonly<T> = { readonly [P in keyof T]: T[P]};
```

## Record
将K中所有的属性的值转换为T类型
`type Record<K extends keyof any, T> = { [P in K]: T}`

## Pick
从T中取出一系列K的属性
`type Pick<T, K extends keyof T> = { [P in K]: T[P]}`

## Exclude
在ts2.8中引入了一个条件类型，示例如下
`T extends U ? X : Y`
以上语句的意思就是如果T是U的子类型的话，那么就会返回X，否则返回Y。
甚至可以组合多个

```js
type TypeName<T> = 
    T extends string ? 'string' :
    T extends number ? 'number':
    T extends boolean ? 'boolean' :
    T extends undefined ? 'undefined' :
    T extends Function ? 'function' :
    'object';
```

对于联合类型来说会自动分发条件，例如`T extends U ? X : Y`，T可能是`A | B`的联合类型，那实际情况就变成(A extends U ? X : Y) | (B extends U ? X : Y)
有了以上的了解，我们再来理解下面的工具泛型。
来看看Exclude源码
`type Exclude<T, U> = T extends U ? never : T;`
结合实例
`type T = Exclude<1 | 2, 1 | 3>  // -> 2`
很轻松地得出结果，2 根据代码和示例我们可以推断出Exclude的作用是从T中找出U中没有的元素，换种更加贴近语义的说法是从T中排除U

## Extract
根据源码我们推断出Extract的作用是提取出T包含在U中的元素，换种更加贴近语义的说法就是从T中提取出U，源码如下。
`type Extract<T, U> = T extends U ? T : never;`

## Omit(未包含)
用之前的Pick和Exclude进行组合，实现忽略对象某些属性功能，源码如下
```js
type Omit<T, K> = Pick<T, Exclude<keyof T, K>>
// 使用
type Foo = Omit<{name: string, age: number}, 'name'> // => { age: number };
```

## ReturnType
在阅读源码之前我们需要了解一下infer这个关键字，在条件类型语句中，我们可以用infer声明一个类型变量并且对他进行使用，我们可以用它获取函数的返回类型，源码如下
```js
type ReturnType<T> = T extends (...args:any[]) => infer R ? R : any;
```

其实这里的infer R就是声明一个变量来承载传入函数签名的返回值类型，简单说就是用它取到函数返回值的类型方便之后使用。
具体用法

```js
function foo(x: number): Array<number> {
    return [x];
}
type fn = ReturnType<typeof foo>;
```

## AxiosReturnType(未包含)
开发经常使用axios进行封装API层请求，通常是一个函数返回一个AxiosPromise<Resp>，现在我想取到他的Resp类型，根据上一个工具泛型的知识我们可以这样写

```js
import { AxiosPromise } from 'axios'
type AxiosReturnType<T> = T extends (...args: any[]) => AxiosPromise<infer R> ? R : any;
type Resp = AxiosReturnType<Api> // 泛型参数中传入你的Api请求函数
```