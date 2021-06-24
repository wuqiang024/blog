querystring这个模块用来做url查询参数的解析

## 查询参数解析: querystring.parse()
>> 参数: querystring.parse(str, sep, eq, options)
>
第四个参数几乎不会用到

```
var querystring = require('querystring');
var str = 'nick=casper&age=24';
var obj = querystring.parse(str);
```
再来看下sep, eq有什么用，相当于可以替换&,=为自定义字符

```
var str1 = 'nick=casper&age=24&extra=name-chyingp|country-cn';
var obj1 = querystring.parse(str1);
var obj2 = querystring.parse(obj1.extra, '|', '-');
console.log(JSON.stringify(obj2, null, 4));
```

输出如下

```
{
	'name': 'chyingp',
	'country': 'cn'
}
```

## 查询参数拼接： querystring.stringify()
>> querystring.stringify（obj, sep, eq)
>
相当于parse逆向操作