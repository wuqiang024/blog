## 安装和使用mongoose
***

```bash
npm install mongoose -S
```

## 使用
***

```javascript
var mongoose = require('mongoose');
mongoose.connect('mongodb://user:pass@localhost:27017/blog');
```

## Schema允许的类型有
***
* String
* Number
* Date
* ObjectId
* Mixed
* Boolean
* Buffer
* Array

## 自定义实例方法
***

```javascript
var userSchema = new Schema({...});

userSchema.methods.findUserByType = function(name, cb) {
	return this.find({type: name}, cb);
};
userSchema.statics.findUserByType = function(name, cb) {};
var User = mongoose.model('User', userSchema);
var userEntity = new User({...});

user.findUserByType(function(err, users){})
```

## 查询辅助
***
可以自定义一个查询的辅助函数，他和实体的方法类似，但是供mongoose查询使用

```javascript
userSchema.query.byName = function(name) {
	return this.find({name: new RegEx(name, 'ig')})
}
userSchema.find().byName('leung').exec(function(err, users) {
	err && return console.error(err);
	console.log(users);
})
```

## 索引
***
MongoDb支持第二个索引，在使用mongoose的时候，可以在定义Schema的时候定义索引。

```javascript
// 定义方法一
var userSchema = new Schema({
	name: String,
	pass: String,
	email: String,
	createTime: {type: Date, index: true},
	type: String
});

// 定义方法二
userSchema.index({createTime: true, lastLogin: -1});
```

Mongoose会在程序启动的时候，对于每个定义了索引的字段自动调用ensureIndex函数。当不需要这些索引的时候，可以使用下列4种方式关闭索引。

```javascript
mongoose.connect('mongodb://user:pass@localhost:port/database', {config: {autIndex:false }});
mongoose.createConnection('mongodb://user:pass@localhost:port/database', {config: {autoIndex:false }});
userSchema.set('autoIndex', false);
new Schema({...}, {autoIndex: false});
```

## 虚拟字段
*** 
虚拟字段可以让你很方便的在文档中存取，但是不会写入数据库中。getter方法在格式化或合并字段的时候很有用，而setter方法在反格式化或者将多个值合并的时候很有用。

```javascript
var personSchema = new Schema({...});
var Person = mongoose.model('Person', personShema);
personSchema.virtual('name.fuulName').get(function(){
	console.log(this);
	return this.name.firstName + ' ' + this.name.lastName;
});
var me = new Person({...});
console.log(me);
console.log(me.name.fullName);
```
虚拟字段的setter方法会在其他检校之前使用，因此，即使字段必须的，虚拟字段也会正常执行。

`只有非虚拟字段才可以在查询或字段选择中使用`


## 配置项
***
Schema有许多可配置的配置项，可以在新建Schema时或者直接设置。

```javascript
new Schema({...}, options);
var schema = new Schema({...});
schema.set(option, value);
```

有效的配置项:
* autoIndex
* capped
* collection
* emitIndexErrors
* id
* _id
* minimize
* read
* safe
* shardKey
* strict
* toJSON
* toObject
* typeKey
* validateBeforeSave
* versionKey
* skipVersioning
* timestamps

## validate
***
Mongoose中，在定义Schema的时候，允许用户自定义字段的检验规则。当在Schema中定义校验规则的时候，需要遵守下列规则。

* 校验规则需要在Schema中定义
* 校验会在save操作前调用
* 可以通过doc.validate(callback)和doc.validateSync()手动校验
* 未定义校验规则的字段不会校验，除非是required必要字段。
* 校验时异步递归的，当使用Model.save时，子文档的校验规则将会立即调用，有错误时，执行的Model.save会收到错误信息。
* 校验时自定义的。
  普通的校验定义:

 ```javascript
 var personSchema = new Schema({
 	name: {
 		type: String,
 		validate: {
 			validator: function(value) {
 				return ...
 			},
 			message: '{VALUE} is not valid'
 		},
 		required: [true, 'name required']
 	},
 	phone: {
 		type: String,
 		validate: {
 			validator: function(v) {
 				return ...
 			},
 			message: '${VALUE} is not a valid phone number'
 		},
 		required:[true, 'phone required']
 	},
 	gender: {
 		type: String,
 		enum: {
 			values: ['female', 'male'],
 			message: '${VALUE} is not a valid gender'
 		}
 	},
 }, {collection: 'person'})
 ```

 mongoose中的内置验证如下:

 >> 
 * 所有的Schema都有required校验规则，必要校验器会调用Schema的checkRequired()函数去校验该字段的值是否符合规则。
 * Number类型有min和max。
 * String类型有enum, minlength, maxlength, match的校验器.
 >

 * required: 必填校验
 可以传入的参数为: [boolean, String]. 当只传true或者false时，用于定义该字段是否为必填；当传入第二个参数String时，该信息作为校验失败的错误提示语。

 * enum： 枚举类型校验。
 可以传入的参数为: Array/Object。当类型为Array时，指定该字段的值必须在该数组中；当传入类型为Object时，可以定义两个键值对： values 和 message, values 的类型为Array, 指定字段的值必须在数组values中，message指定校验失败的错误提示语

 * validator: 校验的对象
 该对象包括两个键值对:
 ** validate 可以是正则表达式，也可以是一个函数
 ** message 则是错误信息提示语。

 * min, max: 对数字类型的进行大小校验，第二个参数可以为字符串，作为错误提示语。
 * minlength, maxlength: 对字符串类型进行长度校验，第二个参数可以为字符串，作为错误提示语。
 * match: 接受一个正则表达式进行校验，第二个参数可以为字符串，作为错误提示语。
 * trim: 字符串在校验时,是否去除前后字符串。默认为false。

 使用mongoose的自动校验功能，可以省去去多校验操作。
 以前直接使用mongodb去操作数据，每次读取操作都要打开，关闭数据库，但是当王爷刷新/访问过于频繁时，就会出现数据库来不及关闭，又开始新的查询，就有可能出现error。

 现在使用mongoose，打开数据库的连接后，db就会一直处于连接状态，不需要在访问时才打开连接，操作后关闭连接，error也不会再出现了。而且代码易读性也提高了不少
