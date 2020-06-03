## 取得Get Request的Query Strings:
***

```
GET /test?name=fred&tel=012049204

app.get('/test', function(req, res) {
	console.log(req.query.name);
	console.log(req.query.tel);
})
```

如果是透过表单而且是用POST method:

```
<form action="/test?id=3" method="post">
	<input type="text" name="name" value="fred">
	<input type="text" name="tel" value="020200">
	<input type="submit" value="submit"
</form>

app.post('/test', function(req, res) {
	console.log(req.query.id);
	console.log(req.body.name);
	console.log(req.body.tel);
})
```

如果是通过param

```
GET /hello/fred/092929

app.get('/hello/:name/:tel', function(req, res) {
	console.log(req.params.name);
	console.log(req.params.tel);
})
```
