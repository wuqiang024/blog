# Kotlin入门JSON字符串的解析
***
json是APP进行网络通信常见的数据交互方式，Android也自带了json格式的处理工具包org.json，该工具包主要提供了JSONObject(json对象)与JSONArray(json数组)的解析处置。下面分别介绍这两个工具类的用法。

## JSONObject
***
JSONObject的常用方法如下所示:
构造函数：从指定字符串构造出一个JSONObject对象。
getJSONObject: 获取指定名称的JSONObject对象
getString: 获取指定名称的字符串
getInt: 获取指定名称的整数
getDouble: 获取指定名称的布尔数
getJSONArray: 获取指定名称的JSONArray数组
put: 添加一个JSONObject对象
toString: 把当前JSONObject输出为一个json字符串。

## JSONArray
***
JSONArray的常用方法如下所示：
length(): 获取JSONArray数组对象的长度。
getJSONObject: 获取JSONArray数组对象在指定位置处的JSONObject对象。

https://blog.csdn.net/aqi00/article/details/83689104