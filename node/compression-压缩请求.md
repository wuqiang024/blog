## 安装
***

```bash
npm install compression -S
```

## 使用
***
compression([options]);
根据options参数，将所有请求的response进行压缩

该中间件不会对请求头信息中包含`Cache-Control`缓存信息和`no-transform`指令的请求进行压缩。
因为压缩会改变主体。

`options`属性
支持如下属性，还支持node.js中zlib压缩中的属性

chunkSize: 大小，默认zlib.Z_DEFAULT_CHUNK或16384.
`zlib来自var zlib = require('zlib')`

filter: 值是一个方法fn(req, res) 返回true或者false,判断是否压缩
默认情况res.getHeader('Content-Type')类型请求返回true

例:

```javascript
app.use(compression({
	filter:(req, res)=>{
		if(req.headers['x-no-compression']) {
			// 过滤掉了请求头中包含'x-no-compression'
			return false;
		} else {
			return true;
		}
	}
}));
```

level: 压缩级别，级别越高，压缩 效果越好。但时间越长，属性值是integer类型，范围是0-9，0为不压缩。
’-1‘为特殊值，相当于取默认压缩至（去效果和性能的折中，大概6级左右)

memLevel: 内存分配级别，inter类型，范围1-9，默认是8级

strategy: 优化压缩算法，只影响压缩性能，不影响压缩正确性。
1. zlib.Z_DEFAULT_STRATEGY 正常
2. zlib.Z_FILTERED 使用过滤后的数据，数据会很分散，即使这样，优化效果也很好，该值算法介于zlib.Z_DEFAULT_STRATEGY和zlib.Z_HUFFMAN_ONLY之间。
3. zlib.Z_FIXED 阻止动态Huffman coding的使用，一些特殊程序可能会用到
4. zlib.Z_HUFFMAN_ONLY 只能使用Huffman coding
5. zlib.Z_RLE 将匹配距离限制设置为1，与zlib设计一样，但是能更好的压缩png图片

windowBits: 窗口大小(历史缓冲区的大小), 默认zlib_Z_DEFAULT_WINDOWBITS或者15
值越大，将消耗更多内存，同时带来更好的压缩效果。

方法:

```bash
compression.filter(req, res)
```

调用默认过滤器，以下方法可以在过滤完自定义之后再进行默认过滤
```javascript
compression({
	filter:(req, res)=>{
		if(req.headers['x-no-compression']) {
			return false;
		}
		return compression.filter(req, res)
	}
})

res.flush
```
强制将压缩刷新到客户端

## 在nginx中如何开启
nginx也支持gizp压缩，下面为配置方法
```sh
# on为启用，off为关闭
gzip on;

# 设置允许压缩的页面最小字节数，页面字节数从header头中的content-length中进行获取。默认值是0,不管页面多大都压缩。建议设置成大于1K的字节数，小于1K可能越压越大。
gzip_min_length 1k;

# 获取多少内存用于缓存压缩结果，’4 16k' 表示以16k*4为单位获得。
gzip_buffer 4 16k;

# gzip压缩比(1-9)，越小压缩效果越差，但是越大处理越慢，所以一般取中间值
gzip_comp_level 5;

# 对特定的MIME类型生效，其中'text/html'被系统强制启用。
gzip_types text/plain application/json application/x-javascript application/xml text/javascript
```
