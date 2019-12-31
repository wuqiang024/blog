# 带有function的JSON对象的序列化与还原
JSON对象的序列化和反序列化相信大家都很熟悉了。基本的api是JSON.parse与JSON.stringify

```js
var json = {
	uiModule: 'http://www.a.com',
	login: 'true',
	mainSubjectId: 3004,
	type: 'all',
	tagList: [
		{'tagName': 'xiaoc'}
	]
}

var s = JSON.stringify(json);
```

会输出序列化后的字符串。

`"json = {
	uiModule: 'http://www.a.com',
	login: 'true',
	mainSubjectId: 3004,
	type: 'all',
	tagList: [
		{'tagName': 'xiaoc'}
	]
}"`

```js
JSON.parse(s)
```
则会返回JSON字符串。![https://pic002.cnblogs.com/images/2012/290046/2012112811371022.png](https://pic002.cnblogs.com/images/2012/290046/2012112811371022.png)。
ok,到现在为止都没啥问题，处理的很好，但是我现在有这么一个对象。

```js
var json = {
	name: 'json',
	getName: function() {
		return this.name;
	}
}
```

通过`JSON.stringify(json)`输出啥:
`"json{'name':'json'}"`，把getName弄丢了。怎么办呢，其实大家都没注意到JSON.stringify还有些参数。

```
JSON.stringify(value [, replacer] [, space])

value

Required. A JavaScript value, usually an object or array, to be converted.

replacer

Optional. A function or array that transforms the results.

If replacer is a function, JSON.stringify calls the function, passing in the key and value of each member. The return value is used instead of the original value. If the function returns undefined, the member is excluded. The key for the root object is an empty string: "".

If replacer is an array, only members with key values in the array will be converted. The order in which the members are converted is the same as the order of the keys in the array. The replacer array is ignored when thevalue argument is also an array.

space

Optional. Adds indentation, white space, and line break characters to the return-value JSON text to make it easier to read.

If space is omitted, the return-value text is generated without any extra white space.

If space is a number, the return-value text is indented with the specified number of white spaces at each level. Ifspace is greater than 10, text is indented 10 spaces.

If space is a non-empty string, such as '\t', the return-value text is indented with the characters in the string at each level.

If space is a string that is longer than 10 characters, the first 10 characters are used.
```

那我们现在就可以把函数也序列化了。

```js
var s = JSON.stringify(json, function(key, val) {
	if (typeof val === 'function') {
		return val + '';
	}
	return val;
})
```

此时会返回`"{"name":"json","getName":"function (){\n     return this.name;   \n  }"}"`

此时再直接JSON.parse(s)。输出的是
![https://pic002.cnblogs.com/images/2012/290046/2012112811562165.png](https://pic002.cnblogs.com/images/2012/290046/2012112811562165.png)

其实JSON.parse和JSON.stringify一样有一些其他参数。

```
JSON.parse(text [, reviver])

text
  Required. A valid JSON string.
reviver
  Optional. A function that transforms the results. This function is called for each member of the object. If a member contains nested objects, the nested objects are transformed before the parent object is. For each member, the following occurs:
If reviver returns a valid value, the member value is replaced with the transformed value.
If reviver returns the same value it received, the member value is not modified.
If reviver returns null or undefined, the member is deleted.
```

那么我们可以这样来还原json对象。

```js
JSON.parse(s, function(k,v) {
	if(v.indexOf && v.indexOf('function') > -1) {
		return eval("function(){ return" + v + "})()")
	}
	return v
})
```

输出![https://pic002.cnblogs.com/images/2012/290046/2012112812240113.png](https://pic002.cnblogs.com/images/2012/290046/2012112812240113.png)

通过这种方式，我们也可以完全深拷贝一个对象了。