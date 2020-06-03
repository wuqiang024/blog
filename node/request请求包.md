request是一个第三方模块，可用于发起http或https请求，可理解成服务端的ajax请求。可用于简单的服务器代理，用法和ajax类似。
在使用之前需要先安装`npm install request -S`

# Get请求

```js
request.get(url, (err, response, body) {
	console.log(body)
})
```

# 多参数设置

```js
exports.get = function(url, options) {
	options = options || {};
	var httpOptions = {
		url: url,
		method: 'get',
		timeout: options.time || 10000,
		headers: options.headers || default_post_header,
		proxy: options.proxy || '',
		agentOptions: agentOptions,
		params: options.params || {}
	}

	if(options.userAgent) {
		httpOptions.header = {
			'User-Agent': userAgent[options.userAgent],
		}
	}

	try {
		request.get(httpOptions, function(err, response, body) {
			if(err) {
				options.callback({status: false, error: err})
			} else {
				options.callback({status: res.statusCode == 200, error: res, data: body})
			}
		}).on('error', logger.error)
	} catch(err) {
		console.log('error')
	}
}
```

# POST请求
request支持application/x-www-form-urlencoded和multilpart/form-data实现表单上传。

application/x-www-form-urlencoded

```js
request.post(url, {form: { key: 'value' }})
request.post(url).form({key: 'value'})
request.post({url:url, form:{key: 'value'}}, function(err, httpResponse, body) {})
```

mutipart/form-data

```js
var formData = {
	my_field: 'my_value',
	my_buffer: new Buffer([1, 2, 3]),
	my_file: fs.createReadStream(path.join(__dirname, '/test.jpg')),
	attachments: [
		fs.createReadStream(path),
		fs.createReadStream(path)
	]
};
request.post({url: url, formData: formData}, function(err, httpResponse, body) {
	if(err) {
		return console.error(err);
	}
	console.log(body);
})
```

# 常用多参数设置

```js
exports.form_post = function(url, postdata, options) {
	return new Promise(resolve, reject) {
		options = options || {};
		var httpOptions = {
			url: url,
			form: postdata,
			method: 'post',
			timeout: options.timeout || 3000,
			headers: options.headers || default_post_header,
			proxy: options.proxy || '',
			agentOptions: agentOptions
		};
		request(httpOptions, function(err, res, body) {
			if(err) {
				reject(err)
			} else {
				if(res.statusCode == 200) {
					resolve(body);
				} else {
					reject(res.statusCode);
				}
			}
		}).on('error', logger.error);
	}
}
```

# 流

```js
request('http://www.sohu.com/1.jpg').pipe(fs.createWriteStream('test.pnt'))
require(url).pipe(fs.createWriteStream('1.json'));
```