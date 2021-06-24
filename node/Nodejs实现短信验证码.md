该接口要求提前在云片后台添加模板，提交短信时，系统会自动匹配审核通过的模板，匹配成功任意一个模板即可发送。系统已提供的默认模板添加签名后可以直接使用。

```js
const https = require('https');
const qs = require('querystring');

var apikey = 'xxx';
var mobile = 'xxx';  // 你要发送的手机号码，多个号码用逗号隔开
var text = '[云片网]您的验证码是1234';  // 你要发送的短信内容
var tpl_id = 1; // 指定发送的模板编号
var tpl_value = {'#code#': '1234', '#company': 'yunpian'}; // 指定发送的模板内容
var code = '1234';  // 语音短信内容
var get_user_info_url = '/v2/user/get.json'; // 查询账户信息https地址
var sms_host = 'sms.yunpian.com';
var voice_host = 'voice.sms.yunpian.com'; // 智能匹配模板发送https地址

send_sms_uri = '/v2/sms/tpl_single_send.json';
send_tpl_sms_uri = '/v2/sms/tpl_tpl_single_send.json';  // 指定模板发送接口https地址
send_voice_uri = '/v2/voice/send.json';

query_user_info(get_user_info_url, apikey);
send_sms(send_sms_uri, apikey, mobile, text);
send_tpl_sms(send_tpl_sms_uri, apikey, mobile, tpl_id, tpl_value);
send_voice_sms(send_voice_uri, apikey, mobile, code);

function query_user_info(uri, apikey) {
	var post_data = {
		'apikey': apikey,
	};
	var content = qs.stringify(post_data);
	post(uri, content, sms_host);
}

function send_sms(uri, apikey, mobile, text) {
	var post_data = {
		'apikey': apikey,
		'mobile': mobile,
		'text': text,
	};
	var content = qs.stringify(post_data);
	post(uri, content, sms_host);
}

function send_tpl_sms(uri, apikey, mobile, tpl_id, tpl_value) {
	var post_data = {
		'apikey': apikey,
		'mobile': mobile,
		'tpl_id': tpl_id,
		'tpl_value': tpl_value
	};
	var content = qs.stringify(post_data);
	post(uri, content, sms_host);
}

function send_voice_sms(uri, apikey, mobile, code) {
	var post_data = {
		'apikey': apikey,
		'mobile': mobile,
		'code': code
	};
	var content = qs.stringify(post_data);
	post(uri, content, voice_host);
}

function post(uri, content ,host) {
	var options = {
		hostname: host,
		port: 443,
		path: uri,
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
		}
	};
	var req = https.request(options, function(res) {
		res.setEncoding('utf8');
		res.on('data', function(chunk) {
			console.log(chunk);
		})
	});
	req.write(content);
	req.end();
}
```
