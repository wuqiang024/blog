<!--
 * @Author: your name
 * @Date: 2021-12-28 11:00:36
 * @LastEditTime: 2021-12-28 11:00:36
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /recoms-is/Users/wuqiang/workspace/blog/常用工具网站/next.md
-->
# next常见问题
***

## 一个响应式的页面，pc 端显示 HeaderBar 组件，m 端不显示，如何处理？
***
在客户端渲染的情况下，判断一下设备类型即可。但是在服务端渲染，在哪里判断设备类型呢？useEffect？不能在里面判断。

方案有二：

采用客户端渲染的处理方式。使用 next/dynamic 动态导入 HeaderBar 组件，这样 HeaderBar 组件将在客户端进行渲染，其它元素依然还是在服务端进行渲染。
依然采用服务端渲染的处理方式。通过 css 的媒体查询，在 m 端对 HeaderBar 进行 display:none，这也是一种处理办法。