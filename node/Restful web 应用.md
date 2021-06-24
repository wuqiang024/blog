# Restful web 应用
* Rest意思是表征状态传输
* 使用正确的HTTP方法，URLs和头部信息来创建语义化RESTful API
* GET /pages: 获取
* POST /pages: 创建
* Get /pages/10: 获取pages10
* PATCH /pages/10: 更新pages10
* PUT /pages/10: 替换pages10
* DELETE /pages/10: 删除pages10

```js
const express = require('express');
const routes = require('./routes');

module.exports = app = express();

app.use(express.json());  // 使用JSON body解析
app.use(express.methodOverride()); // 允许一个查询参数来指定额外的HTTP方法

// 资源使用的路由
app.get('/pages', routes.pages.index);
app.get('/pages/:id', routes.pages.show);
app.post('/pages', routes.pages.create);
app.patch('/pages/:id', routes.pages.patch);
app.put('/pages/:id', routes.pages.update);
app.del('/pages/:id', routes.pages.remove);
```