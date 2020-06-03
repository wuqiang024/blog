## mongoose
***
关于mongoose只要搞明白schema, model, entity三个概念就行了。

* schema: 一种以文件形式存在的数据库模型骨架，不具备数据库的操作能力
* model: 由schema发布生成的模型，具有抽象属性和数据库操作能力
* entity: 由model创建的实例，也能操作数据库

mongoose文档地址:
http://mongoosejs.com/docs/index.html


## mongoose连接数据库
***
文件路径: ./db.js

```
const mongoose = require('mongoose');
mongoose.connect('mongodb:user:password@localhost:port/database');
const db = mongoose.connection;

db.on('error', (err)=>{
	console.log('连接失败');
});

db.on('open', ()=>{
	console.log('连接成功');
});
```

## 构建schema和model
***
文件路径: ./model/User.js
schema其实是对collection的数据格式进行了规范，然后通过这个规范抽象collection模型。
`注意: 很多文章都对于mongoose.model()方法只写两个参数，其实建议最少应该写三个参数, 如果不写第三个参数，会导致当库中不存在collection的时候，会根据ModelName的负数形式创建collection.`

* ModelName: 抽象的模型的名字
* Schema: 创建的Schema变量
* collectionName: 关联的库中的collection名字

```
const mongoose = require('mongoose');
const db = require('./db');
const userSchema = mongoose.Schema({
	name: {type: String},
	age: {type: Number, default: 0}
});
const User = mongoose.model('User', userSchema, 'user');
module.exports = User;
// 导出model以供其他的文件或者方法操作数据库
```

## 数据查询
***
引入User的model，之后不再重复。
```
const User = require('./model/User');
```
代码中均使用Promise的操作，不使用回调函数，不再重复。
Model提供的查询方法列表：
* Model.find()
* Model.findById()
* Model.findByIdAndDelete()
* Model.findByIdAndRemove()
* Model.findByIdAndUpdate()
* Model.findOne()
* Model.findOneAndDelete()
* Model.findOneAndRemove()
* Model.findOneAndUpdate()

1、查询所有文档 find()

```
User.find({}).then((docs)=>{
	console.log(docs);
}).catch((err)=>{
	console.lo(err);
})
```

2、查询符合条件的一条数据 findOne()

```
Usser.findOne({_id: '....'}).then((doc)=>{}).catch((err)=>{})
```

3、通过_id查询 findById()

```
User.findById('...').then((doc)=>{})
```


## 数据插入
***
Model提供的数据插入方法:
* Model.create()
除了使用model提供的create方法外，还可以通过构建Entity实例，插入数据，而Entity实例提供的方法是entity.save()

1、插入一条数据

```
User.create({name:'', age:18}).then((res)=>{})
```

2、插入多条数据

```
const array = [{}, {}];
User.create(array).then((res)=>{})
```

3、通过entity实例保存save()

```
const entity = new User({...});
entity.save().then((res)=>{})
```

## 数据更新
***
Model提供的数据更新方法:
* Model.update()
* Model.updateOne()
* Model.updateMany()

1、更新一条数据

```
let conditions = {name: '...'};
let update = {$set:{name:'...'}};
User.updateOne(conditions, update).then((res)=>{})
```

2、更新所有符合条件的数据updateMany()

```
let conditions = {name: '...'};
let update = {$set:{name:'...'}};
```

3、用update()更新
同updateOne()。默认只更新一条数据


## 数据删除
Model提供的数据删除方法:
* Model.deleteMany()
* Model.deleteOne()
* Model.remove()

1、删除一条数据

```
let conditions = {name:'...'};
User.deleteOne(conditions).then((res)=>{})
```

2、删除多条数据

```
let conditions = {name:'...'};
User.deleteMany(conditions).then((res)=>{});
```

## 高级查询
***

1、查询特定字段
必定会出现
只查询`age`字段

```
User.find({}, 'age').then((res)=>{}).catch((err)=>{});
```

2、条件查询判断
查询年龄大于等于18岁的所有文档

```
let conditions = {age:{$gte:18}};
User.find(conditions).then((docs)=>{});
```

3、查询年龄是16或者17的文档

```
let conditions = {$or:[{age:16}, {age:17}]};
User.find(conditions).then((docs)=>{})
```

## 游标操作和排序
***
1、skip和limit
链式调用方法进行查询

```
User.find().skip(2).limit(2).then((docs)=>{});
```

通过参数配置进行查询

```
User.find({}, null, {skip:2, limit:2}).then((docs)=>{});
```

2、排序
sort 排序 1: 升序  -1: 降序
通过链式调用

```
User.find().sort({age:1}).skip(3).limit(2).then((docs)=>{});
```

通过参数配置:

```
User.find({}, null, {sort:{age:-1}}.then((docs)=>{});
```
```