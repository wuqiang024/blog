<!--
 * @Author: your name
 * @Date: 2022-02-23 12:53:48
 * @LastEditTime: 2022-03-02 12:45:40
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/react/vue和react的数据流与数据绑定.md
-->
# vue与react的数据流与数据绑定
## 数据
就是指的是组件之间的数据流动

## 数据绑定
所谓数据绑定，就是指Model层与View层的映射关系。

`单向数据绑定:` Model的更新会触发View的更新，而View的更新不会触发Model的更新，它们的作用是单向的
单向数据绑定的优缺点:
`优点:` 所有状态变化都可以被记录、跟踪，状态变化通过手动调用触发，源头容易追溯。
`缺点:` 会有很多类似的样板代码，代码量会相应的上升。

`双向数据绑定:` Model的更新会触发View的更新，View的更新也会触发Model的更新，它们的作用是相互的。
`优点:` 在操作表单时使用v-model比较方便，可以省略繁琐或重复的onChange事件去处理每个表单数据的变化（减少代码量）
`缺点:` 属于暗箱操作，无法很好的追踪双向绑定的数据的变化

## Vue数据流与绑定
****
在Vue中，父组件使用props将值传递给子组件后，子组件并不能修改从父组件传递过来的值，而是通过$emit去通知父组件进行修改。所以vue也是属于单向数据流的。
vue一般使用单向绑定: 插值方式{{data}}, v-bind也是单向绑定
vue中也存在双向绑定: v-model。所存在的双向绑定v-model只不过是v-bind:value和v-on:input的语法糖。

## react数据流与绑定
***
在react中，数据流同样是单向传递的。父组件将值传给子组件，但子组件不能修改父组件的值。子组件要想修改父组件的值，只能通过调用从父组件传递过来的方法，从而将值传递给父组件。或者是通过redux, context的方式。