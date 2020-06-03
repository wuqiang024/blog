node有很多读写excel的模块，这里只写常用的模块。

* xlsx: 读取excel
* excel-export: 导出excel

# xlsx读取excel文件
库中提及的一些概念
* workbook对象，指的是整份excel文档。我们在使用js-xlsx读取excel文档之后就会获得workbook对象。
* worksheet对象，指的是excel文档中的表。我们知道一份excel可以包含很多张表，而每张表对应的就是worksheet对象。
* cell对象，指的就是worksheet中的单元格，一个单元格就是一个cell对象。

他们的对应关系如下:

```js
// workbook
{
	SheetNames: ['sheet1', 'sheet2'],
	Sheets: {
		'sheet1': {
			'A1': {},
			'A2'：{}
		},
		'sheet2': {
			'A1': {},
			...
		}
	}
}
```

用法:
1、用XLSX.read读取获取到的excel数据，返回workbook
2、用XLSX.readFile打开excel文件，返回workbook
3、用workbook.SheetNames获取表名
4、用workbook.Sheets[xxx]通过表名获取表格
5、用worksheet[address]操作单元格
6、用XLSX.utils.sheet_to_json针对单个表获取表格数据转换为json格式
7、用XLSX.writeFile(wb, 'output.xlsx')生成新的excel文件

```js
// 读取excel文件
XLSX.read(data, read_opts) // 尝试解析数据
XLSX.readFile(filename, read_opts)  // 尝试读取文件名和解析
```

```js
// 获取excel中的表
var sheetNames = workbook.SheetNames; // 返回['shhet1', 'sheet2']
var worksheet = workbook.Sheets[sheetNames[0]]; // 根据表名获取对应某张表
```

通过worksheet[address]来操作表格，以!开头的key是特殊的字段

```js
// 获取A1单元格对象
let a1 = worksheet['A1']; // 返回{v: 'hello', t:'s', ...}
// 获取A1中的值
a1.v; // 返回hello
worksheet['!ref']; // 获取有效范围，返回'A1:B20'
worksheet['!range']; // 返回range对象，{s:{ r: 0, c: 0}, e: {r: 100, c: 2}}
worksheet['!merges']; // 获取合并过的单元格,返回一个包含range对象的列表
```

获取excel文件中的表转换为json数据。

```js
XLSX.utils.sheet_to_json(worksheet); // 针对单个表，返回序列化json数据
```

## excel-export导出excel

```js
const excelPort = require('excel-export');
const path = require('path');
exports.write = function(req, res, next) {
	var datas = req.data;
	var conf = {};
	var filename = 'filename'; // 只支持字母和数字命名

	conf.cols = [{
		caption: '学号',
		type: 'string',
		width: 20
	}, {
		caption: '姓名',
		type: 'string',
		width: 40
	}];

	var array = [];
	array = [
	]
}