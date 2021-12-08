# 网络请求retrofit2通过post提交json数据
***
使用Retrofit分为四步:
1、创建Retrofit对象
2、创建访问请求
3、发送请求
4、处理结果

## 创建Retrofit对象
***
```java
Retrofit retrofit = new Retrofit.Builder()
    .baseUrl(BASE_URL)
    .addConverterFactory(GsonConverterFactory.create())
    .build();
service = retrofit.create(UserService.class);
```

## 创建访问请求
***
项目中post请求除了键值对，还可能会遇到json/xml的请求，限制上传格式为json/xml，所有要添加头文件headers

```java
@Headers({"Content-Type:application/json;charset=UTF-8"})
@POST("/api/v1/trade/HasAccount.json")
Call<BaseResponse> createCommit(@Body RequestBody route);
```

## 提交数据
***
```java
Gson gson = new Gson();
HashMap<String, String> paramsMap = new HashMap<>();
paramsMap.put("userId", "173");
String strEntity = gson.toJson(paramsMap);
body = RequestBody.create(okhttp3.MediaType.parse("application/json;charset=UTF-8"), strEntity);
Call<BaseResponse> call = api.getService().createCommit(body);
```