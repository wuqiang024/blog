## 简介
***
之前操作时间和日期都是使用moment.js，太大了，200多k，而day.js只有2k左右，非常轻量。
(github)[https://github.com/xx45/dayjs]
支持node和浏览器端使用

## 基本使用
***
安装

```bash
npm install dayjs
```

引入

```javascript
const dayjs = require('dayjs')
```

dayjs本质上是个函数，因此需要直接运行该函数dayjs().


## 解析
对传入的参数解析，解析出来的就是dayjs的对象。

* 解析时间字符串
```javascript
dayjs('2018-05-12');
```

* 解析Unix时间戳
```javascript
dayjs(1200020482003);
```

* 解析Date对象
```javascript
dayjs(new Date(2018,5,3));
```

* 解析dayjs对象
```javascript
dayjs(dayjs());
```

## 克隆
dayjs对象是不可变的，如果要复制对象，需要调用`.clone()`，或者是再解析一个dayjs对象
```javascript
dayjs(dayjs());
dayjs().clone();
```

## 验证有效
返回true或者false
```javascript
dayjs().isValid()
```

## 获取各种时间
* 年: dayjs().year()
* 月: dayjs().month()
* 日: dayjs().date()
* 时: dayjs().hour()
* 分: dayjs().minute()
* 秒: dayjs().second()
* 毫秒: dayjs().millisecond()

## 设置时间
```javascript
// dayjs().set(unit: String, value: Int);
dayjs().set('hour', 1);
dayjs().set('hour', 25).hour() // 会返回 1
```

## 链式操作
因为操作返回的是dayjs对象，所以可以链式调用
比如:

```javascript
dayjs().startOf('month').add(1, 'day').subtract(1, 'year');

```

* 增加
```javascript
dayjs().add(7, 'day').date()
```
上面代码输出后会在原有的日期的基础上加上7天，比如今天5月2日，结果会变成5月7日
同样的操作可以应用到 `year/month/minute/second/`

* 减少
```javascript
dayjs().subtract(7, 'month').month();
```

* 开头时间
```javascript
dayjs().startOf('year');
dayjs().startOf('month').date();
dayjs().startOf('day').date()
```

* 结尾时间
```
dayjs().endOf('year')
dayjs().endOf('month').date()
dayjs().endOf('day').date()
```

## 格式化时间
如果需要格式化时间，则通过.format()即可
```javascript
dayjs().format('[YYYY] MM-DDTHH:mm:ss:ssZ'); // "[2014] 09-08T08:02:17-05:00"
```

* YY 两位数年份
* YYYY 四位数年份
* M 月份 从1开始
* MM 月份，数字前面加上0
* MMM Jan-Dec 简写月份的名称
* D 1-31 月份里的一天
* DD 01-31 月份里的一天，数字前面加上0
* d 0-6 一周中的一天，星期天是0
* dddd 一周中一天的名称，英文全称
* H 0-23  小时
* HH 00-23 小时，数字前面加0
* m 0-59 分钟
* mm 00-59 分钟，数字前面加0
* s 0-59 秒
* ss 00-59 秒，数字前面加0
* Z +5:00  UTC的偏移量
* ZZ +0500 UTC的偏移量，数字前面加0

## 时间差
```javascript
dayjs().diff(Dayjs, unit);
dayjs().diff(dayjs(), 'year'); // 0
```

## 时间戳
获得unix时间戳
```javascript
dayjs().valueOf()
```

## 获得unix秒级时间戳
```javascript
dayjs().unix()
```

## 天数
返回月份的天数
```javascript
dayjs().daysInMonth()
```

## 获取Date对象
```javascript
dayjs().toDate();
```

## 获取数组格式
```javascript
dayjs().toArray(); //[2018, 8, 18, 00, 00, 00, 000];
```

## 获取对象
```javascript
dayjs().toObject(); // { years:2018, ... milliseconds:0} 都为复数
```

## 查询
是否之前
检查一个dayjs对象是否在另一个dayjs对象之前
```javascript
dayjs().isBefore(DayJs);
dayjs().isBefore(dayjs()) // false
```

是否相同
```javascript
dayjs().isSame(Dayjs);
```

是否之后
```javascript
dayjs().isAfter(Dayjs)
```

是否是闰年
```javascript
dayjs().isLeapYear();
dayjs('2000-01-01').isLeapYear(); // true
```