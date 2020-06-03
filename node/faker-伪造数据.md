## 用法
***

### 浏览器端
***

```javascript
<script src="faker.js" type="text/javascript"></script>
<script>
	var randomName = faker.name.findName();
	var randomEmail = faker.internet.email();
	var randomCrd = faker.helpers.createCard();
</script>
```

### nodejs端
***

```javascript
var faker = require('faker');

var randomName = faker.name.findName();
...
```


## API
faker.js有一个超级有用的生成器方法faker.fake()

```javascript
console.log(faker.fake（"{{name.lastname}}, {{name.firstname}}, {{name.suffix}}");
// outputs: "marks, dean sr."
```


## faker.seed()
如果给这个函数传入一个相同的值，那么生成的伪随机数会一样
```javascript
faker.seed(123);
var firstName = faker.random.number();
faker.seed(123);
var secondName = faker.random.number();
// 这两个数值相等
```
