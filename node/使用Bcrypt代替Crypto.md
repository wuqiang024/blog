<!--
 * @Author: your name
 * @Date: 2021-06-24 18:16:30
 * @LastEditTime: 2021-11-29 17:16:47
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /recoms-is-master/Users/wuqiang/workspace/blog/node/使用Bcrypt代替Crypto.md
-->
密码或者机密信息(API)应该使用安全的hash+salt函数(bcrypt)来存储，因为性能和安全原因，这应该是其javascript实现的首选。

```js
// https://www.npmjs.com/package/bcrypt
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