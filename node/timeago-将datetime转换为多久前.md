> timeago.js是一个非常简洁，轻量级，小于2kb的js库，用来将datetime时间转换成类似于xxx时间前的描述字符串，例如:'3小时前'。

* 本地化支持，默认自带中文和英文语言，基本够用；
* 之前xxx时间前，xxx时间后；
* 支持npm方式和浏览器script方式
* 测试用例完善，执行良好；

关于Python的版本，可以看timeago

```
刚刚  12秒前  3分钟前  2小时前  24天前  6月前  3年前  12秒后  3分钟后  2小时后  24天后  6月后  3年后
```

## 使用方法
***
1、下载

```
npm install timeago.js
```

2、引入

```javascript
import timeago from 'timeago.js';
var timeago = require('timeago.js');
<script src="dist/timeago.min.js"></script>
```

3、使用timeago类

```javascript
var timeago = timeago();
timeago.format('2016-06-01');
```

## 高级特性使用
***
1、本地化
默认的语言是英文，这个库自带语言en 和 zh_CN (英文和中文)

```javascript
var timeago = timeago();
timeago.format('2016-06-12', 'zh_CN');
```

2、注册本地语言
你可以自己自定义注册你自己的语言。如下所示，所有的键值都必须存在，不如会报错

```javascript
/ 本地化的字典样式 var test_local_dict = { 'JUST_NOW': ["just now", "a while"], 'SECOND_AGO': ["%s seconds ago", "in %s seconds"], 'A_MINUTE_AGO': ["1 minute ago", "in 1 minute"], 'MINUTES_AGO': ["%s minutes ago", "in %s minutes"], 'AN_HOUR_AGO': ["1 hour ago", "in 1 hour"], 'HOURS_AGO': ["%s hours ago", "in %s hours"], 'A_DAY_AGO': ["1 day ago", "in 1 day"], 'DAYS_AGO': ["%s days ago", "in %s days"], 'A_MONTH_AGO': ["1 month ago", "in 1 month"], 'MONTHS_AGO': ["%s months ago", "in %s months"], 'A_YEAR_AGO': ["1 year ago", "in 1 year"], 'YEARS_AGO': ["%s years ago", "in %s years"] } var timeago = timeago(); timeago.register('test_local', test_local_dict); timeago.format('2016-06-12', 'test_local');
```

3、设置相对日期
timeago 默认是相对于当前事件的，当然也可以自己设置相对的时间，如下所示：

```javascript
var timeago = timeago('2016-06-10 12:12:12'); // 在这里设置相对时间 timeago.format('2016-06-12', 'zh_CN');
```

4、格式化时间戳

```javascript
timeago().format(new Date().getTime() - 11 * 1000 * 60 * 60); // will get '11 hours ago'
```