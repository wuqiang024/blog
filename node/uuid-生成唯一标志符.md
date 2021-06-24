## 安装
***

```bash
npm install uuid
```

### version1(timestamp):
***

根据时间戳生成唯一标志符

```javascript
const uuidv1 = require('uuid/v1');
uuidv1();  // 3b99e3e0-7598-11e8-90be-95472fb3ecbd
```

### version3(namespace):
***

```javascript
const uuidv3 = require('uuid/v3');
// 通过预定义的DNS 域名空间
uuidv3('hello.example.com', uuidv3.DNS);  // '9125a8dc-52ee-365b-a5aa-81b0b3681cf6'
// 通过预定义的URL命名空间
uuidv3('http://example.com/hello', uuidv3.URL);  //  'c6235813-3ba4-3801-ae84-e0a6ebb7d138'
// 通过普通命名空间
const MY_NAMESPACE = '1b671a64-40d5-491e-99b0-da01ff1f3341';
uuidv3('hello, world', MY_NAMESPACE);  // 'e8b5a51d-11c8-3310-a6ab-367563f20686'
```

### version4(random)
***

```javascript
const uuidv4 = require('uuid/v4');
uuidv4();
```
