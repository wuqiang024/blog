ECMAScript2015也称为ES6,是一个花了6年时间完成的主要版本。ES2019将会发布。新功能包括Object.fromEntries(), trimStart(), trimEnd(), flat, flatMap(), symbol对象的description属性，可选的catch绑定等。
这些功能已经在最新版本的firefox和chrome实现，并且他们也可以被转换，以便旧版浏览器能处理他们。

# Object.fromEntries()
为了便于将对象转换成数组，ES2017引入了Object.entries()方法，此方法将对象作为参数，并以[key, value]的形式返回。
例如:
```js
const obj = {one: 1, two: 2, three: 3};
console.log(Object.entries(obj));
// [['one', 1], ['two', 2], ['three', 3]]
```
ES2019引入Object.fromEntries()方法，来做反操作，将键值对列表转为对象。

# trimStart() and trimEnd()
trimStart()和trimEnd()方法在实现上与trimLeft()和trimRight()相同，这些方法目前处于第四阶段，将被添加到规范中，以便与padStart()和pardEnd()保持一致。

# flat() and flatMap()
flat()方法可以将多维数组展平成一维数组。
```js
const arr = ['a', 'b', ['c', 'd']];
arr.flat(); // ['a', 'b', 'c', 'd']
```
flat()还可以接受一个可选参数，该参数指定嵌套数组应该被展平的级别数。如果未提供参数，则将使用默认值1.
`请注意，如果提供的数组中有空值，他们将会被丢弃。`

flatMap()方法将map()和flat()组合成一个方法。他首先使用提供的函数的返回值创建一个新数组，然后连接该数组的所有子数组元素。
```js
const arr = [4.25, 19.99, 25.5];
console.log(arr.flatMap(value => [Math.round(value)]));
// [4, 20, 26]
```

数组将被展平的深度为1，如果要从结果中删除项目，只需返回一个空数组。
```js
const arr = [...];
arr.flatMap(value => {
    if(value >= 10) {
        return []
    } else {
        return Math.round(value);
    }
})
```

# Symbol对象的description属性
在创建Symbol时，可以为调试目的向其添加description。
ES2019中为Symbol对象添加了只读属性description,该对象返回包含Symbol描述的字符串。
```js
let sym = Symbol('foo');
console.log(sym.description); // foo
```

# 可选的catch
try catch 语句中的catch有时候并没有用，为了避免错误，catch后还是要跟catch(err)。ES2019可以省略catch周围的括号。
```js
try {
    ...
} catch {
    ...
}
```