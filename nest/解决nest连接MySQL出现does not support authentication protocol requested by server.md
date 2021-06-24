MySQL是最流行的关系型数据库管理系统，在WEB应用方面MySQL是最好的RDBMS(Relational Database Management System): 关系型数据库管理系统。

在安装完成后，我们现在一般都使用Navicat来连接数据库，可惜出现以下错误: 1251-Client does not support authentication protocol requested by server; consider upgrading MySQL client。

出现上述问题的原因是: mysql8之前的版本中加密规则是mysql_native_password，而在mysql8之后，加密规则是caching_sha2_password。
解决方案是: 把mysql用户名登录密码规则还原成mysql_native_password

```sh
alter user '用户名'@'%' identified with mysql_native_password by '密码';
```

假如我的用户名是admin,密码是123456，那么，修改的规则如下:

```sh
alter user 'admin'@'%' identified with mysql_native_password by '123456'
```

其中还有'用户名'@'%' 和 '用户名`@'localhost'的区别，一个是任意连接，一个是本地连接。

最后，刷新权限: `flush privileges`;