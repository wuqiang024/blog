# vue2.0与3.0的差异
***

1、3.0比2.0快2倍
2、3.0去掉了filter,没有beforeCreate和created，用setup替代
3、setup里面没有this
4、支持多个子节点fragment
5、单独功能可以抽离，替代了mixin，优于mixin，解决了上下反复横跳
6、proxy实现响应式，不需要set和delete，兼容性不好
7、响应式不区分数组和对象
8、支持ie12以上
9、composition api可以和options api同时存在
10、reactivity是可以作为单独的库使用的