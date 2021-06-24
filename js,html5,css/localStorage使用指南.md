# localStorage使用指南--你所不知道的localStorage
***
localStorage是只读的。类似于sessionStorage。区别在于，数据存储在localStorage是无期限的。而当页面会话结束---也就是页面关闭时，数据存储在sessionStorage会被清除。

常见的四个API也很简单。

```js
localStorage.setItem('name', 'Tom'); // 增加一个name数据项
localStorage.getItem('name'); // 读取localStorage里的name数据项
localStorage.removeItem('name'); // 移除localStorage里的name数据项
localStorage.clear() // 清除所有的localStorage选项。
```

## localStorage对象和Storage对象
***
首先来说说Storage对象，Storage提供了访问特定域名下的会话存储(sessionStorage)和本地存储(localStorage)的功能，例如，可以添加，修改或删除存储的数据项。

Storage对象通过对Window.sessionStorage和Window.localStorage属性使用(更确切的说，在支持的浏览器中，Window对象实现了`WindowLocalStorage`和`WindowSessionStorage`对象并挂在其`localStorage`和`sessionStorage`属性下)----调用其中任一对象会创建相应的Storage对象，通过Storage对象，可以设置，获取和移动数据项。对于每个源(origin)sessionStorage和localStorage使用不同的Storage对象--独立运行和控制。

说的直接一点。localStorage对象其实就是就是Storage对象的实例对象。我们可以在开发者工具的控制台(Console)面板中输入Storage，localStorage，查看这两个对象，再输入`localStorage instance of Storage`或者`localStorage.constructor == Storage`查看这两个对象的关系。

可以看出localStorage是Storage的实例对象。

## localStorage一些不为人知的方法
***
### 访问和设置数据
***
`localStorage`对象是简单的键值存储，类似于对象。键和值始终是字符串。您可以像对象一样，使用点语法`.`或者中括号`[]`的形式访问这些值，也可以使用`localStorage.getItem()`和`localStorage.setItem()`方法访问或设置这些值。下面的代码是等价的。

```js
// 设置值
localStorage.myCat = 'Tom';
localStorage['myCat'] = 'Tom';
localStorage.setItEM('myCat', 'Tom');

// 获取值
localStorage.mycat
localStorage['mycat']
localStorage.getItem('mycat')
```

但是官方建议使用`setItem`, `getItem`,'removeItem`这些API，来防止与使用普通对象作为键值存储相关的陷阱。

### 使用localStorage.hasOwnProperty()检查localStorage中存储的数据里是否保存某个值
***
`hasOwnProperty()`方法检查对象自身属性中是否具有指定的属性，返回一个布尔值。换句话说就是检查localStorage中存储的数据里是否保存某个值。

假设，我们的本地存储了`mycat`数据，没存`youcat`数据。之前你要判断本地是否存储了`youcat`数据，你可能需要这么做。
`localStorage.getItem('youcat'); // null`
有了`hasOwnProperty()`方法就简单多了。

```js
localStorage.hasOwnProperty('mycat'); // true
localStorage.hasOwnProperty('youcat'); // false
```

### Object.keys(localStorage)查看localStorage中存储数据所有的键
***
想看到localStorage中存储了哪些键，我们可以直接用`Object.keys(localStorage)`查看，很方便。

### localStorage.key(index)方法
***
读取第index个数据的名字或键，经常从0开始索引。`localStorage.key(5)`

333 localStorage.length属性
***
查看localStorage里存储了多少个数据。

## 其他实用技巧
***
接下来说说实际应用的技巧

### 将JSON存储到localStorage里
***
为了方便起见，我们通常会将一个大数组或对象存储到localStorage中，而localStorage只能存储字符串，我们可以使用JSON方法对存取值进行转换。

```js
var users = [
    { name: 'xiaoming', grade: 1 },
    { name: 'teemo', grade: 3 }
];

// 存数据
usersStr = JSON.stringify(users); // 将JSON转为字符串
localStorage.users = usersStr; // 将字符串存到localStorage users键下

// 取数据
var newUsers = JSON.parse(localStorage.users); // 转为JSON
```

### 为localStorage设置过期时间
***
localStorage原生是不支持设置过期时间的，想要设置的话，就只能自己来封装一层逻辑来实现。

```js
function set(key, value) {
    var curtime = new Date().getTime(); // 获取当前时间
    localStorage.setItem(key, JSON.Stringify({val: value, time: curtime}));
}

function get(key,exp) { // exp是设置的过期时间
    var val = localStorage.getItem(key); // 获取存储的元素
    var dataobj = JSON.parse(val); // 解析出json对象
    if(new Date().getTime() - dataobj.time > exp) { // 如果当前时间-减去存储的元素在创建时候设置的时间>过期时间
        console.log('expires'); // 提示过期
    } else {
        ...
    }
}
```

原理就是在存值的时候附带一个设置的时间，取值的时候传一个时间过期时间(毫秒),和存在的时间作比较，然后做相应的操作。

### storage事件
***
当存储数据发生变化的时候，会触发`storage`事件。值得特别注意的是，该事件不会导致数据变化的当前页面触发。如果浏览器同时打开一个域名下的多个页面，当其中的一个页面改变sessionStorage或localStorage的数据时，其他所有页面的storage事件都会被触发，而原始页面并不触发storage事件。可以通过这种机制，实现多个窗口之间的通信。(当然ie这个特例除外，他包含本身也会触发storage事件)。例如我们全局监听`storage`事件。

```js
window.addEventListener('storage', function onStorageChange(event) {
    console.log(event.key); // 更新的键值
    console.log(event.oldValue); // 更新前的值，如果该键为新增，则这个属性为null
    console.log(event.newOld); // 更新后的值，如果该键被删除，这个属性为null
    console.log(event.url); // 原始触发storage事件的那个网页的网址。
})
```