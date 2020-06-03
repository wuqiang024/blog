在开发过程中，我们经常需要对用户输入数据进行各种验证，比如判断Email是否合法，判断URL是否合法等，validator是一个验证工具的集合包，包含了非常多的常用验证器。

# 使用validator
我们可以直接require validator，这样就引入了所有验证器集合。

```js
const validator = require('validator');
validator.isEmail('foo@bar.com'); // true
```

我们也可以按照需求require个别验证器。

```js
const isEmail = require('validator/lib/isEmail');
isEmail('foo@bar.com'); // true
```

验证器列表

|-验证器-|-说明-|
|- contains(str, seed)-|-检查包含-|
|-equals(str,comparison)-|-检查相等-|

https://github.com/chriso/validator.js