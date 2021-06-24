我们知道validator库可以用来验证字符串是否是Email,URL等，在开发中，除了字符串，我们还需要对更复杂的数据进行验证。比如需要Object满足哪些属性，每个属性都是什么类型等，这些条件称之为数据模式验证。

在对数据的模式验证领域有专门的标准，叫做JSON Schema。就是按照JSON Schema标准声明一个模式对象，然后使用模式验证工具去验证目标数据。

# ajv
ajv是一个非常流行的JSON Schema验证工具，并且拥有非常出众的性能表现。下面的例子中，我们使用avj来验证用户输入的表单数据是否合法。

```js
const Ajv = require('avj');
const schema = {
	type: 'object',
	required: ['username', 'email', 'password'],
	properties: {
		username: {
			type: 'string',
			minLength: 4
		},
		email: {
			type: 'string',
			format: 'email',
		},
		password: {
			type: 'string',
			minLength: 6
		},
		age: {
			type: 'integer',
			minimun: 0
		},
		sex: {
			enum: ['boy', 'girl', 'secret'],
			default: 'secret'
		}
	},
};

let ajv = new Ajv();
let validate = ajv.compile(schema);
let valid = validate(data);
if(!valid) console.log(validate.errors);
```

在上述代码中，我们声明了一个数据模式schema，这个模式要求目标数据为一个对象，对象可以有五个字段username,email,password,age,sex，并分别定义了五个字段的类型和数据格式要求，并且其中username, email, password必填。然后我们使用这个模式去验证用户输入的数据data是否满足我们的需求。

注意:
* JSON Schema是一个声明模式描述对象的标准，并非一个库
* ajv是个JSON Schema标准验证器的实现，除了ajv还有很多其他库
* 代码中的schema是使用JSON Schema生成的模式描述对象
* 代码中data是我们要进行检查的数据。

`使用ajv验证JSON Schema可以将模式配置信息保存在.json文件中，因为JSON Schema模式是声明式的。`

https://github.com/epoberezkin/ajv