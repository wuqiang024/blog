# node-schedule定时任务包
## 安装
```sh
cnpm install node-schedule -S
```

```js
*    *    *    *    *    *
┬    ┬    ┬    ┬    ┬    ┬
│    │    │    │    │    │
│    │    │    │    │    └ day of week (0 - 7) (0 or 7 is Sun)
│    │    │    │    └───── month (1 - 12)
│    │    │    └────────── day of month (1 - 31)
│    │    └─────────────── hour (0 - 23)
│    └──────────────────── minute (0 - 59)
└───────────────────────── second (0 - 59, OPTIONAL)
```

```js
const schedule = require('node-schedule');
// 每当分钟指向42的时候开始执行计划任务(例如19:42,20:42)
const j = schedule.scheduleJob('42 * * * *', function() {
	console.log('test')
})
```

```js
const j = schedule.scheduleJob('0 17 ? * 0, 4-6', function() {
	console.log('test');
})
```

```js
// 每隔5分钟执行一次任务
const js = schedule.scheduleJob('*/5 * * * *', function() {
	console.log('test');
})
```

## 基于特定时间执行计划任务
```js
const schedule = require('node-schedule');
const date = new Date(2012, 11, 21, 5, 30, 0);;
const j = schedule.scheduleJob(date, function() {
	console.log('test');
})
```

## Recurrence Rule Scheduling
```js
const schedule = require('node-schedule');
const rule = new schedule.RecurrenceRule();
rule.minute = 42;

var j = schedule.scheduleJob(rule, function(){})
```

```js
var rule = new schedule.RecurrenceRule();
rule.dayOfWeek = [0, new schedule.Range(4,6)];
rule.hour = 17;
rule.minute = 0;

var j = schedule.scheduleJob(rule, function() {})
```

## RecurrenceRule 属性
* second (0-59)
* minute (0-59)
* hour (0-23)
* date (1-31)
* month (0-11)
* year

## 基于对象字面量的操作
```js
// 下面定时任务将在每个周日的14:30分运行
var j = schedule.scheduleJob({hour: 14, minute: 30, dayOfWeek: 0}, function() {
	console.log('test');
})
```

## 设定开始时间和结束时间的定时任务
```js
// 该任务将在5秒后开始运行，10秒后停止。
let startTime = new Date(Date.now() + 5000);
let endTime = new Date(startTime.getTime() + 5000);
var j = schedule.scheduleJob({start: startTime, end: endTime, rule: '*/1 * * * * *'}, function() {
	console.log('time out');
});
```

## 取消定时任务
```js
j.cancel()
```