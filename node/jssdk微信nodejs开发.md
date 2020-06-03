# 安装

```sh
cnpm install redis -S
```

# demo

```js
const redis = require('redis');
const client = redis.createClient('6379', '127.0.0.1');

client.auth('password');
client.set('hello', 'value'); // 设置键值对
client.expire('hello', 10);  // 设置过期时间
client.exists('key'); // 判断键是否存在
client.del('key1');
client.get('hello');

// string
set // set(key, value);
get // get('key') => value/null
del // 删除存储在给定键中的值(任意类型) 1/0 del('key');
incrby // 将键存储的值加上整数 incrby('key', increment)
decrby // 将键存储的值减去整数 decrby('key', increment)
incrbyfloat // 将键存储的值加上浮点数 incrbyfloat('key', increment)
append // 将值value追加到给定键当前存储值的末尾 append('key', 'new-value')
getrange // 获取指定键index范围内的所有字符组成的字串 getrange('key', 'start-index', 'end-index')
setrange // 将指定键值从指定偏移量开始的字串设为指定值 setrange('key', 'offset', 'new-string')

// list
rpush // 将给定值推入列表的右端，当前列表长度 rpush('key', 'value1', 'value2') (支持数组赋值)
lrange // 获取列表在给定范围上的所有值 array lrange('key', 0, -1) (返回所有值)
lindex // 获取列表在给定位置上的单个元素 lindex('key', 1)
lpop // 从列表左端弹出一个值，并返回被弹出的值lpop('key')
rpop // 从列表右端弹出一个值，并返回被弹出的值rpop('key')
ltrim // 将列表按指定的index范围裁减 ltrim('key', 'start', 'end')

// set
sadd // 将给定元素添加到集合中 插入元素数量 sadd('key', 'value1', 'value2')(不支持数组赋值)(元素不允许重复)
smembers // 返回集合中包含的所有元素 array(无须) smembers('key')
sismenber // 检查给定的元素是否存在集合中 sismenber('key', 'value')
srem // 如果给定的元素在集合中 则移除此元素 1/0 srem('key', 'value')
scad // 返回集合包含的元素数量 scad('key')
spop // 随机移除集合中的一个元素 并返回此元素 spop('key')
smove // 集合元素的迁移 smove('source-key', 'dest-key', 'item')


// hash
hset // 在散列里面关联起给定的键值对 1(新增)/0(更新) hset('hash-key', 'sub-key', 'value') (不支持数组，字符串)
hget // 获取指定散列键的值 hget('hash-key', 'sub-key')
hgetall // 获取散列包含的键值对 json hgetall('hash-key')
hdel // 如果给定键存在于散列里面，则移除这个键 hdel('hash-key', 'sub-key')
hmset // 为散列里的一个或多个键设定值 OK hmset('hash-key', obj)
hmget // 从散列里获取一个或多个键的值 array hmget('hash-key', array)
hlen // 返回散列包含的键值对数量 hlen('hash-key')
hexists // 检查给定键是否在散列中 1/0 hexists('hash-key', 'sub-key')
hkeys // 获取散列包含的所有键 array hkeys('hash-key')
hvals // 获取散列包含的所有值 hvals('hash-key')
hincrby // 将存储的键值以指定数量增加 返回增长后的值 hincrby('hash-key', 'sub-key', increment)
hincrbyfloat // 以浮点数增加

// keys 命令组
del // 删除一个或多个keys 返回被删除的数量 del('key1', 'key2')
exists // 查询一个key是否存在 1/0 exists('key')
expire // 设置一个key的过期的秒数 1/0 expire('key', seconds)
pexpire // 设置一个key的过期的毫秒数
expireat // 设置一个unix时间戳的过期时间 1/0 expireat('key', timestamp)
pexpireat // 设置一个unix时间戳的过期时间(毫秒) 1/0 pexpireat('key', milliseconds-timestamp)
persist // 移除key的过期时间 1/0 persist('key')
sort // 对队列，集合，有序集合排序 排序完成的队列等 sort('key'[, pattern, limit offset count])
flushdb // 清空当前数据库
```