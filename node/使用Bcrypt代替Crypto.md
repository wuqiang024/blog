密码或者机密信息(API)应该使用安全的hash+salt函数(bcrypt)来存储，因为性能和安全原因，这应该是其javascript实现的首选。

```js
// 使用10个哈希回合异步生成安全密码
bcrypt.hash('myPassword', 10, function(err, has) {
	// 在用户记录中存储安全哈希
});

bcrypt.compare('somePassword', hash, function(err, match) {
	if(match) {
		// 密码匹配
	} else {
		// 密码不匹配
	}
})
```