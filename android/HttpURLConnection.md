# HttpURLConnection
***
过去在android上有两种发送http请求的方式，一种是`HttpURLConnection`,另一种是`HttpClient`，不过由于HttpClient的API数量过多，扩展困难等特点，越来越不建议我们用这种方式，在android6.0系统中，HttpClient被完全移除了。

```java
override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  // do something
  btn.setOnClickListener {
    sendHttpRequestConnection()
  }
}

private fun sendHttpRequestConnection() {
  thread {
    var connection: HttpURLConnection? = null
    try {
      val response = StringBuilder()
      val url = URL("https://www.baidu.com")
      val connection = url.openConnection() as HttpURLConnection
      connection.connectTimeout = 8000
      connection.readTimeout = 8000
      val input = connection.inputStream
      val reader = BufferedReader(InputStreamReader(input))
      reader.use {
        reader.forEachLine {
          response.append(it)
        }
      }
      showReponse(response.toString())
    } catch (e: Exception) {
      e.printStackTrace()
    } finally {
      connection?.disconnection()
    }
  }
}

private fun showResponse(response: String) {
  runOnUiThread {
    textView.text = response
  }
}
```
如果想要提交数据给服务器应该怎么办，其实也不复杂，只需要将Http请求方法改为POST,并在获取输入流之前把要提交的数据写出即可。注意，每条数据都要以键值对的形式存在。数据与数据之间用`&`符号隔开。

```java
connection.requestMethod = "POST"
val output = DataOutPutStream(connection.outputStream)
output.writeBytes("username=admin&password=123456")
```