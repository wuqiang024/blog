# 介绍两大神器!----使用json-server和faker.js模拟REST API
***
今天发现了一个神器----json-server!在它的帮助下可以在很短时间内搭建一个REST API,然后就可以让前端在不依赖后端的情况下进行开发。

## JSON-Server
***
简单来说,JSON-Server是一个Node模块，运行Express服务器，你可以指定一个json文件作为api的数据源。
举个例子:
我们想做一个app，用来管理客户信息，实现简单的CRUD功能(create/retrive/update/delete),比如:
* 获取客户信息
* 增加一个客户
* 删除一个客户
* 更新客户信息

接下来我们用json-server完成这一系列动作。

### 安装JSON-Server
***
`npm install -g json-server`
新建一个文件夹同时cd它:
`mkdir customer-manager && cd customer-manager`
新建一个json文件，然后存放一点数据进去。、:
`touch customer.json`

```json
{
    "customers": [
        {"id": 1, "first_name": "John", "last_name": "Smith", "phone": "158118181" }
    ]
}
```

### 开启JSON-Server功能
***
所有你要做的事情就只是让json-server指向这个customer.json就ok了。
`json-server customer.json`
然后出现提示就成功了。

另外，JSON-Server很酷的一点就是支持各种GET/PUT/UPDATE/DELETE的请求。

```js
// GET
fetch(url).then(function(res){
    return res.json()
}).then(function(json) { return json}).catch(function(err) {
    console.log(err);
})

// POST
fetch(url, {
    method: 'post',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.Stringify(obj)
}).then(function(res) {
    return res.json()
}).then(function(json) {
    return json;
}).catch(function(err) {
    console.log(err)
})

// PUT
fetch(url, {
    method: 'put',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.Stringify(obj)
}).then(function(res) {
    return res.json()
}).then(function(json) {
    return json;
}).catch(function(err) {
    console.log(err)
})
```

## Faker.js
***
如果要自己瞎编API数据的话也是比较烦恼，用faker.js就可以轻松解决这个问题，他可以帮助你自动生成大量fake的json数据，作为后端数据。
`npm install faker`
现在我们用javascript生成一个包含50个客户数据的json文件。

```js
var faker = require('faker');

function generateCustomers() {
    var customers = [];
    for(var id = 0; id < 50; i++) {
        var firstName = faker.name.firstName();
        var lastName = faker.name.firstName();
        var phoneNumber = faker.phone.phoneNumberFormat();

        customers.push({
            "id": id,
            "first_name": firstName,
            "last_name": lastName,
            "phone": phoneNumber
        })
    }
    
    return { "customers": customers };
}

module.exports = generateCustomers;
```

然后让json-server指向这个js文件。
`json-server customer.js`

这样你就可以在`http://localhost:3000/customers`里看到50个数据了。

参考地址:
`https://github.com/marak/Faker.js/`