# 网络请求json参数处理
***

## 自定义json字符串
***
在json数据解析时要把请求数据变为json格式，可以直接用String + String的方式来实现如下。

```java
String json = "{" + "\"" + "status" + "\"" + ":" + "200" + "}";
```

这样写很麻烦而且容易出错，可以采用以下方式实现:

```java
JSONObject params = new JSONObject();
try {
  params.put("code", "12");
  params.put("type", "31");
} catch(JSONException e) {
  back.OnFailure("error")
} catch(IOException e) {
  back.OnFailure("error")
}
```

提交的时候用这种方式`httputils.post(url, params.toString())`。

## 对于返回的数据是json格式的，直接可以进行json解析，如一个json字符串

```java
JSONObject obj = new JSONObject(result);  // 将json字符串转换成JSONObject格式
String resCode = obj.get("result_code").toString()
// 或者可以用
String resCode = obj.getString("result_code");
// 层层解析
JSONObject obj1 = new JSONObject(retcode);
int status = obj1.getInt("status")
String code = obj1.getString("code")
```