# Object.freeze与const之间的区别
***
![https://segmentfault.com/img/remote/1460000019348513](https://segmentfault.com/img/remote/1460000019348513)

自ES6发布以来，ES6给JS带来了一些新的特性和方法。对于JavaScript开发者来说，这些特性能够很好地改善我们的工作流程及效率，其中的特性就包括Object.freeze()方法和const。

一些开发人员特别是新手们会认为这两个功能的工作方式是一样的，但其实并不是。

## 综述
***
const和Object.freeze()完全不同。

```js
const user = 'Bolaji Ayodeyi';
user = 'Joe amide';
```

这个例子会出现Uncaught TypeError，因为我们正在尝试重新分配使用const关键字声明的变量user,这样做是无效的。

这个例子使用var是可以工作的，但是使用const不能。

## const的问题
***
使用const声明的对象仅能阻止其重新分配，但是不能使其声明的对象具有不可变性(能够阻止更改其属性)。

```js
const user = {
    first_name: 'bolaji',
    last_name: 'ayodejj',
    email: 'hi@sohu.com',
    net_worth: 2000
}

user.last_name = 'Sanmson'; // ok
console.log(user); // user is mutated
```

尽管我们无法重新分配这个名为user的变量，但是我们仍然可以改变其对象本身。

```js
const user = {
    user_name: 'botsee'; // error
}
```

我们肯定希望对象具有无法修改或删除的属性，const无法实现这样的功能，但是Object.freeze()可以。

## Object.freeze()
***
要禁用对象的任何更改，我们需要使用Object.freeze()。

```js
const user = {
    first_name: 'bolaji',
    last_name: 'ayodeji',
    email: 'hi@sohu.com',
    net_worth: 2000
}
Object.freeze(user);
user.last_name = 'Samson'; // error
```

## 具有嵌套属性的对象实际上并未冻结
***
Object.freeze()只是做了浅层冻结，当遇到具有嵌套属性的对象的时候，我们需要递归Object.freeze来冻结具有嵌套属性的对象。

```js
const user = {
    first_name: 'a',
    last_name: 'b',
    contact: {
        email: 'email',
        telephone: 15811881,
    }
}

Object.freeze(user);
user.first_name = 'c'; // error;
user.contact.telephone = '124'; // ok
```

因此，当具有嵌套属性的对象时，Object.freeze()并不能完全冻结对象。

要完全冻结具有嵌套属性的对象，你可以编写自己的库或使用已有的库来冻结对象，如Deepfreeze或immutable-js。

https://github.com/substack/deep-freeze
https://github.com/immutable-js/immutable-js