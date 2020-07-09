# 加快Vue项目的开发速度
***
## 巧用Webpack
***
`webpack`是实现我们前端项目工程化的基础，但其实它的用处远不止这些，我们可以通过webpack来帮我们做一些自动化的事情。首先我们要了解`require.context()`这个API。

### require.context()
***
> 您可以使用require.context()函数创建自己的上下文。它允许你进入一个目录进行检索，一个标志用于指示是否应该搜索子目录，还有一个正则表达式来匹配文件。

其实是webpack通过解析`require()`的调用，提取出来如下这些信息。

```js
Directory: ./template
Regular expression: /^.*\.ejs$/
```

然后来创建我们自己的上下文，什么意思呢，就是`我们可以通过这个方法筛选出来我们需要的文件并且读取`。

下面我们来简单看一看使用:

```js
/**
 * @param directory 要搜索的文件夹目录不能是变量，否则在编译阶段无法定位目录
 * @param useSubdirectories 是否搜索子目录
 * @param regExp 匹配文件的正则表达式
 * @return function 返回一个具有resolve, keys, id三个属性的方法
 *         resolve() 它返回请求被解析后得到的模块id
 *         keys() 它返回一个数组，由所有符合上下文模块处理的请求组成
 *         id 是上下文模块里面所包含的模块id， 它可能在你使用module.hot.accept的时候被用到
 **/
require.context('demo', useSubdirectories = false, regExp = /\.js$/);
// 创建了一个包含了demo文件夹(不包含子目录)下面的，所有以'js'结尾的，能被require请求到的文件的上下文。
```

不要困惑，接下来我们来探讨在项目中怎么使用。

### 组织路由
***
对于vue中的路由，大家都很熟悉，类似于声明式的配置文件，其实已经很简洁了。现在我们让他更简洁。

1、分割路由
首先为了方便我们的管理，我们把route目录下的文件分割为以下结构:

```js
router // 路由文件夹
    |__index.js // 路由组织器: 用来初始化路由等
    |__common.js // 通用路由: 声明通用路由
    |__modules // 业务逻辑模块: 所有的业务逻辑模块
        |__index.js  // 自动化处理文件: 自动导入路由的核心文件
        |__home.js // 业务模块home: 业务模块
        |__a.js // 业务模块a
```

2、modules文件夹中处理业务模块
modules文件夹中存放着我们所有的业务逻辑模块，至于业务逻辑模块怎么分，我相信大家都有一套自己的标准。我们通过上面提到的`require.context()`接下来编写自动化的核心部分`index.js`。

```js
const files = require.context('.', true, /\.js$/);
console.log(files.keys()) // ['./home.js'] 返回一个数组
let configRouters = [];

files.keys().forEach( key => {
    if(key === './index.js') return
    configRouters = configRouters.concat(files(key).default) // 读取出文件中的default模块
})

export default configRouters; // 抛出一个Vue-router期待的结构的数组
```

自动化部分写完了，那业务组件部分怎么写，更简单了。

```js
import Frame from '@/views/frame/Frame';
import Home from '@/views/index/index';

export default [
    {
        path: '/index',
        name: '首页',
        redirect: '/index',
        component: Frame,
        children: [
            {
                path: '',
                component: Home
            }
        ]
    }
]
```

3、common路由处理，我们的项目中有一大堆公共的路由需要处理，比如404, 503等等路由我们都在common.js中进行处理。

```js
export default [
    // 默认页面
    {
        path: '/',
        redirect: '/index',
        hidden: true
    },
    // 无权限页面
    {
        path: '/nopermission',
        name: 'nopermission',
        component: () => import('@/views/NoPermission')
    },
    // 404
    {
        path: '*',
        name: 'lost',
        component: () => import('@/views/404')
    }
]
```

4、路由初始化这是我们的最后一步了，用来初始化我们的路由。

```js
import Vue from 'vue';
import VueRouter from 'vue-router';
import RouterConfig from './modules';  // 引入业务逻辑模块
import CommonRouters from './common';  // 引入通用模块
Vue.use(VueRouter);

export default new VueRouter({
    mode: 'history',  // 需要服务端支持
    scrollBehavior: () => {y: 0}),
    routes: RouterConfig.concat(CommonRouters)
})
```

估计有些朋友代码写到这里还不知道这样写的好处到底在哪里。我们来描述这样一个场景，比如按照这种结构来划分模块。正常的情况我们是创建完home.js要手动的把这个模块import到路由文件声明的地方去使用，但是有了上面的这个index.js，在使用的时候你只需要去创建一个home.js并抛出一个符合VueRouter规范的数组，剩下的就不用管了。import RouterConfig from './modules' 引入业务逻辑模块已经帮你处理完了。另外扩展的话你还可以把hooks拿出来单独作为一个文件。

### 全局组件统一声明
***
同样的道理，有了上面的经验，我们照葫芦画瓢来处理一下我们的全局组件。

1、组织结构

```js
components // 组件文件夹
    |__xxx.vue // 其他组件
    |__global  // 全局组件
        |__index.js // 自动化处理文件
        |__demo.vue // 全局demo组件
```

2、global处理

```js
import Vue from 'vue';
let contexts = require.context('.', false, /\.vue\$/);
context.keys().forEach(component => {
    let componentEntity = context(component).default;
    // 使用内置的组件名称进行全局组件注册
    Vue.component(componentEntity.name, componentEntity)
})
```
3、使用说明
这个使用起来就简单了，直接在app.js引用这个文件就行。

## 发挥Mixins的威力
***
Vue中的混入mixin是一种提供分发vue组件中可复用功能的非常灵活的方式。听说在3.0版本中会以Hooks的形式实现，但这并不妨碍它的强大。这里主要来讨论mixins能在什么情况下帮助我们。

`通用mixins`
如果我们有大量的表格页面，有非常多可以复用的例如`分页`，`表格高度`，`加载方法`,`loading`等一大堆的东西。下面可以整理出一个简单通用混入list.js.

```js
const list = {
    data() {
        return {
            loading: false,
            pageNo: 1,
            pageSize: 15,
            totalCount: 0,
            pageSizes: [15, 20, 25, 30], // 页长数
            pageLayout: 'total, sizes, pre, pager, next, jumper', // 分页布局
            list: []
        }
    },
    methods: {
        handleSizeChange(val) { // 分页回调事件
            this.pageSize = val;
        },
        handleCurrentChange(val) {
            this.pageNo = val
        },
        /**
         * 表格数据请求成功的回调，处理完公共的部分(分页，loading取消)之后把控制权交给页面
         * @param {*} apiResult
         * @returns {*} promise
         */

        listSuccessCb(apiResult = {}) {
             return new Promise(resolve, reject) => {
                 let tmpList = []; // 临时list
                 try {
                     this.loading = false
                     resolve(tmpList)
                 } catch(e) {
                     reject(e)
                 }
             })
         },
         /**
          * 处理异常情况
          * ==> 简单处理 仅仅是对表格处理为空以及取消loading
          */
         listExceptioonCb(error) {
             this.loading = false;
             console.error(error())
         }
    },
    created() {
        this.$nextTick().then(() => {
            // todo
        })
    }
}

export default list;
```

下面我们直接在组件中使用这个mixins

```js
import mixin from '@mixins/list' // 引入
import {getList} from '@/api/demo'
export default {
    name: 'mixins-demo',
    mixins: [mixin], // 使用mixins
    data() {
        return {}
    },
    methods: {
        load() {},
    },
    created() {}
}
```
使用了mixins之后的一个简单的有Loading,分页，数据的表格大概就只需要上面这些代码。

`mixins做公共数据的管理`
有些时候我们有一些公共的数据它可能3，4个模块使用但是又达不到全局的这种规模。这个时候我们就可以用mixins去管理他们，比如我们有几个模块要使用用户类型这个列表，我们来使用mixins来实现共享。

```js
// types.js
import { getTypes } from '@/api/demo';
export default {
    data() {
        return {
            types: [] // {name:'', value:''}
        }
    },
    methods: {
        getAllTypesList() {
            getApiList().then(result => {
                this.types = result; // 假设result就是我们要使用的数据
            }).catch(err => {
                console.log(err)
            })
        }
    },
    created() {
        this.getAllTypesList()
    }
}
```

在组件中引用

```js
import typeMixin from '@/mixins/types'
export default {
    name: 'template',
    data() {
        return {}
    },
    mixins:[typeMixin],
    methods: {}
}
```

至于mixins中的数据我们可以在组件中直接使用。

```html
<el-select v-model="type" clearable placeholder="请选择类型">
    <el-option v-for="item in types" :key="item.id" :label="item.templateName" :value="item.id">
    </el-option>
</el-select>
```

这样我们就可以不用vuex来去管理那些只有在模块之间复用几次的数据，而且非常方便去取我们想要的数据，连定义都省了。但是这有一个缺点，就是每次都会去重新请求这些数据，如果你不在乎这一点点瑕疵的话，我觉得用起来完全是ok的。

注意: mixin虽然是简单的，但是注释和引用一定要做好，不然的话新成员进入团队大概还是一脸的懵逼，而且不利于后期的维护。也是一把双刃剑。另外:全局mixins一定要慎用，如果不是必须要用的话我还是不建议使用。

## 进一步封装组件
***
大家都知道组件化的最大好处就是高度的可复用性和灵活性。但是组件怎么封装好，封装到什么程度让我们更方便。这是没有标准答案的。我们只有根据高内聚，低耦合的这个指导思想来对我们的业务通用组件进行封装，让我们的业务页面结构更加的简洁，加快我们的开发效率。封装多一点的话页面可能会变成这样。

```html
<template>
    <box-content>
        <!-- 头部标题部分 -->
        <page-title>
            <bread-crumb></bread-crumb>
        </page-title>
        <!-- 表格部分 -->
        <div>
            <base-table></base-table>    
        </div>
    </box-content>
</template>
```

有什么东西一目了然。

`无状态组件`
最容易引起我们封装欲望的就是无状态组件，例如我们除去header,menu之后的content部分。没有什么需要复杂的交互，但是我们每个页面又得写。

```html
<template>
    <div :class="[contentClass]">
        <el-row>
            <el-col :span="24>
                <div class="box">
                    <div class="box-body">
                        <slot></slot>
                    </div>
                <div>
            </el-col>
        </el-row>
    </div>
</template>
```

上面的这个处理非常的简单，但是你在项目中会非常频繁的使用到，那么这个封装就很有必要了。

`ElementUI table组件封装`
ElementUI中的组件其实已经封装的非常优秀了，但是表格使用的时候还是有一堆的代码看起来不需要在业务中重复写。封装起来靠配置来进行表格的书写我觉得就差不多了。