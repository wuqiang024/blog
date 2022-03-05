<!--
 * @Author: your name
 * @Date: 2022-03-02 12:46:51
 * @LastEditTime: 2022-03-02 13:12:14
 * @LastEditors: your name
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/js,html5,css/js隐式转化的问题.md
-->
# JS中鲜为人知的问题: [] == ![]结果为true，而{} == !{}却为false
***
```js
console.log([] == ![]) // true
console.log({} == !{}) // false
```

在比较字符串、数值和布尔值的相等性时问题还比较简单。但是在涉及到对象时，就复杂了。

1、如果有一个操作符是布尔值，则在比较相等性之前将其转为数值--false转为0，而true转为1；
2、如果一个操作数是字符串，另一个操作是数值，在比较相等性之前先将字符串转为数值
3、如果一个操作数是对象，另一个不是，则调用对象的valueOf()方法，用得到的基本类型按照前面的规则进行比较。

这个操作符在进行比较时要遵循以下规则
1、null和undefined是相等的
2、要比较相等性之前，不能将null和undefined转换成其他任何值
3、如果又一个操作符是NaN，则相等操作符返回false,不等操作符返回true。`重要提示: 即使两个操作数都是NaN，相等操作符也返回false，因为按照规则，NaN不等于NaN`
4、如果两个操作数都是对象，则比较它们是不是同一个对象，如果两个操作数都指向同一个对象，则返回true，否则返回false

比较运算x == y, 其中x和y是值，产生true或false，这样的比较按如下方式进行。
1、若Type(x)和Type(y)相同，则
**  a、若Type(x)为undefined，返回true
**  b、若Type(x)为null, 返回true
**  c、若Type(x)为Number，则
**  **  i、若x为NaN，返回false
**  **  ii、若y为NaN，返回false
**  **  iii、若x和y为相等数值，返回true
**  **  iv、若x为+0，y为-0，返回true
**  **  v、若x为-0，y为+0，返回true
**  **  vi、返回false
**  d、若Type(x)为string，则当x和y为完全相同的字符串序列时返回true,否则返回false
**  e、若Type(x)为boolean，当x和y同为true或false时返回true,否则返回false
**  f、当x和y为同一引用对象时返回true,否则返回false
2、若x为null,而且y为undefined，返回true
3、若x为undefined,而且y为null，返回true
4、若Type(x)为Number, Type(y)为String，则将字符串转为数字后进行对比
5、若其中一个为boolean类型，则将boolean类型转为数字后进行对比
6、若其中一个为String或Number，另一个为Object类型，则将Object类型用valueOf()和toString()转换后再进行对比

对于空数组, 转为数字后返回的是0，如果只有一个元素，而且这个元素可以转为数字，则返回这个数字，其他都返回NaN
对于空对象, 转换为`[object Object]`后，返回的数字是NaN。