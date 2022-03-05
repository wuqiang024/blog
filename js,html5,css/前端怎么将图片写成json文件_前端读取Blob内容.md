<!--
 * @Author: your name
 * @Date: 2022-03-02 13:21:59
 * @LastEditTime: 2022-03-02 14:07:39
 * @LastEditors: your name
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/js,html5,css/前端怎么将图片写成json文件_前端读取Blob内容.md
-->
# 前端怎么将图片写成json文件_前端读取Blob内容
***
前端由于安全方面的原因，不能直接对文件进行写操作，但是在实际业务需求中，难免会碰到各种各样文件的下载、预览，如果服务端下载文件是以流的形式传递到前端，前端通常是将流转为objectURL，借用a标签的download属性，进行文件下载。但是有时候会碰到下载文件处理失败的场景，这样服务端消息的返回格式不再是流，而是json，此时前端虽然可以正常导出文件，但是文件内容是服务端返回的消息，处置不怎么妥当，这个时候，能有读取流的方法就好了。

## 二进制文件下载
***
普通的二进制文件下载：首先需要将请求头的response-type设置为blob，其次，在接收到响应消息时，可以调用以下方法。

```js
function download(blob) {
  let url = URL.createObjectURL(blob)
  let a = document.createElement('a')
  a.setAttribute('download', url)
  a.href = url
  a.style.display = 'none'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  // 每次调用URL.createObjectURL都会创建一个新的URL对象，浏览器内存中会保持对该对象对引用
  // 只有在document销毁时才会释放此部分内存
  // 在考虑性能对情况下，在url使用结束后，最好释放此部分内存
  URL.revokeObjectURL(url)
}
```

## 二进制文件对读取
***
上述只是二进制文件一般对下载方式，当服务端传回对响应类型`Content-Type = application/json`时，我们仍以二进制对方式去解析数据，会导致导出内容出问题，比如Excel中，内容为服务器响应的消息，因此，我们在处理服务器响应内容时，需要做前置的拦截。

1、声明一个blob变量

```js
var debug = { hello: "world" };
var blob = new Blob([JSON.stringify(debug, null, 2)], {type: 'application/json'})
```

blob内容的读取，主要有两种方式，FileReader和Response。

## FileReader
***
FileReader顾名思义，这个对象就是用来读取文件内容的，兼容性较好，有以下几种读取方式:
`readAsArrayBuffer`、`readAsBinaryString`、`readAsDataURL`、`readAsText`.

```js
var reader = new FileReader()
reader.addEventListener('loaded', function(e) {
  console.log(e.target.result);
})
reader.readAsText(blob)
```

## Response
***
Response是Fetch API的一个接口，呈现的是对一次请求数据对响应。浏览器兼容性比FileReader要差点，支持Chrome 42+、FireFox 39+。
Response实例化
```js
let myResponse = new Response(body, init)
```
Response实现了body接口，所以在实例化Response时，可以调用body.blob(),body.formData(),body.json(),body.text()序列化返回值，返回值是一个Promise。具体实现方法如下:
```js
var blobReader = new Response(blob).json()
blobReader.then(res => {
  console.log(res)
})
```

## 小结
***
有了解析服务器返回值对方法，我们在下载文件时，就可以多判断服务器返回值的content-type，如果返回值不是blob，我们可以做一些自定义处理。
