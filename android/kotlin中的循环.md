# kotlin中的循环
***

## for循环
```kotlin
for(i in 1..n) {}
```

这里的`1..n`指的是[1,n] 包含n,而`for(i in 1 until n)`指的是[1, n), 不包含n.

也可以用for遍历集合中的值。

```kotlin
val list = listOf(...);
for(s in list) {}
```

如果想要带着index一起遍历的话.

```
for ((index, element) in list.withIndex()) {}
```

还有一个比较特殊的语法`forEach`。

```
val list = listOf(...)
list.forEach {
  print("$it")
}
```

## while循环
***
while循环与java中一致。

## Repeat循环
这是kotlin相对于java新加入的特性。取代`for(int i = 0; i < 5; i++)`工作。

```kotlin
repeat(5) { i -> {
  println("循环进行第${i+1}次")
}}
```

再说说跳跃语法。
kotlin引入了标签的概念，可以直接控制程序中应该执行的代码是什么。
标签后面用@注明。

```kotlin
loop@ for(i in 1..100){
    for(j in 1..100){
        if(...) break@loop
    }
}
```
这段代码会跳出带有标签loop@的循环, continue与break用法一样。

## return
***

```kotlin
fun foo() {
    ints.forEach lit@ {
        if (it == 0) return@lit
        print(it)
    }
}
```

```kotlin
fun foo() {
    ints.forEach {
        if (it == 0) return@forEach
        print(it)
    }
}
```

这两段代码效果一样。

还可以使用匿名函数直接返回值。

```kotlin
fun foo() {
    ints.forEach(fun(value: Int) {
        if (value == 0) return
        print(value)
    })
}
```

