## 安装
***

```bash
npm install ejs
```

## 用法
***

```javascript
let ejs = require('ejs'),
	people = ['geddy', 'neil', 'alex'],
	html = ejs.render('<%= people.join(","); %>', {people: people});
```

浏览器端如下:

```javascript
<script src="ejs.js"></script>
<script>
	let people = ['geddy', 'neil', 'alex'],
		html = ejs.render('<%= people.join(",") %>', {people: people});
</script>
```

```html
<ul>
	<% users.forEach(function(user) { %> 
		<%- include('user/show', {user: user}); %>
	<%}) %>
</ul>



## 最新版EJS的include函数已支持参数传递
***
最新版的express中partial函数已经被移除，使用include可以实现同样的效果

```javascript
<% var user = users[0];
	include user/home
%>
```

但是EJS2.0+版本已经支持这样的写法

```javascript
<%- include('user/home', {user:user[0]}) %>
```
