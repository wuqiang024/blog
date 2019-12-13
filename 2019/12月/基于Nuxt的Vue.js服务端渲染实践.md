# 服务端渲染
服务端渲染不是一个新的概念(Server Side Render),在单页面(SPA)还没有流行起来的时候，页面就是通过服务端渲染好，并传递给浏览器的。当用户需要访问新的页面时，需要再次请求服务器，返回新的页面。

为了优化体验，开发者们开始采用JS在前端完成渲染过程，用前后端分离的手段，使后端更专注于数据，而前端注重处理展示，通过设计良好的API以及AJAX技术完成前后端的交互。jQuery, React, Vue, Angular等框架应运而生。

这些框架给开发者带来了巨大便利，但是对于一些论坛，资讯网站，或是企业官网来说，他们对搜索引擎优化(SEO)有强烈的要求，而前端渲染技术无法满足他们的需求。如果无法通过搜索引擎的搜索输出自身的内容，那么网站的价值就大打折扣。要解决这类问题，还是需要服务端渲染。

Vue.js推出后，其数据驱动和组件化思想，以及简洁易上手的特性给开发者带来了巨大便利，Vue.js官方提供的`vue-server-renderer`可以用来进行服务端渲染的工作，但是需要增加额外的工作量，开发体验有待提高，而Nuxt.js推出后，这个问题被很好的解决了。

# Nuxt.js简介
Nuxt.js是一个基于Vue的通用应用框架，Nuxt.js预设了利用Vue.js开发服务端渲染的应用所需要的设置，并且可以一键生成静态站点。同时,Nuxt.js的热加载机制可以使开发者非常便利的进行网站开发。

Nuxt.js于2016年10月25号发布。

## 简单上手
Vue.js的`vue-cli`工具可以方便的让我们使用现成的模板初始化Vue.js项目。
而Nuxt.js团队已经为我们提供了初始化Nuxt.js项目的模板，安装`vue-cli`后，只需要在命令行中输入
`vue init nuxt/starter <projectName>`
即可完成项目的创建工作，然后进入项目目录执行以下命令
`cnpm instal`
`npm run dev`
Nuxt.js会使用3000端口运行服务，在浏览器输入`http://localhost:3000`就可以看到带有Nuxt.js的logo的原始的页面了。

## 项目目录
完成了一个简单的Hello World项目后，我们进一步来研究Nuxt.js。进入Nuxt.js项目后，项目目录如下：

![http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVH2tHRAe4PRMoJxJb5YPFCCl0A3pqiafOpPkvbWgqlBYno05abCaIXZ7A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVH2tHRAe4PRMoJxJb5YPFCCl0A3pqiafOpPkvbWgqlBYno05abCaIXZ7A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

下面简要介绍下各个目录的作用:
* .nuxt/: 用于存放Nuxt.js的核心库文件。例如，你可以在这个目录下找到`server.js`文件，描述了Nuxt.js进行服务端渲染的逻辑。router.js文件包含一张自动生成的路由表。
* assets/: 用于存放静态资源，该目录下的资源使用webpack构建。
* components/: 存放项目中的各种组件。注意，只有在这个目录下的文件才能被称为组件。
* layouts/: 创建自定义的页面布局，可以在这个目录下创建全局页面的统一布局，或者是错误页布局。如果需要在布局中渲染pages目录中的路由页面，需要在布局文件中加上<nuxt />标签
* middleware/ : 放置自定义的中间件，会在加载组件之前调用
* pages/: 在这个目录下，Nuxt.js会根据目录的结构生成vue-router路由。
* plugins/: 可以在这个目录中放置自定义插件，在根Vue对象实例化之前运行。例如，可以将项目中的埋点逻辑封装成一个插件，放置在这个目录中，并在Nuxt.config.js中加载。
* static/: 不使用webpack构建的静态资源，会映射到根路径下，如robots.txt
* store/: 存放Vuex状态树
* nuxt.config.js: Nuxt.js的配置文件

## Nuxt渲染流程
Nuxt.js通过一系列构建于Vue之上的方法进行服务端渲染，具体流程如下:

1、调用nuxtServerInit方法
当请求打入时，最先调用的即使nuxtServerInit方法，可以通过这个方法预先将服务器的数据保存，如已经登录的用户信息等。另外，这个方法中也可以执行异步操作，并等待数据解析后返回。

2、Middleware层
经过第一步后，请求会进入Middleware层，在该层中有三步操作:
* 读取 nuxt.config.js中全局middleware字段的配置，并调用相应的中间件方法
* 匹配并加装与请求相对应的layout
* 调用layout和page的中间件方法

3、调用validate方法
在这一步可以对请求参数进行检验，或是对第一步中服务器下发的数据进行校验，如果校验失败，将抛出404页面。

4、调用fetch及asyncData方法
这两个方法都会在组件加载前被调用，他们的职责各有不同，asyncData用来异步的进行组件数据的初始化工作，而fetch方法偏向于异步获取数据后修改Vuex中的状态

我们在Nuxt.js源码util.js中可以看到以下方法

```js
export function applyAsyncData(Component, asyncData = {}) {
	const ComponentData = Component.options.data || noopData;
	Component.options.data = function() {
		const data = ComponentData.call(this);
		return { ...data, ...asyncData };
	}
	if(Component._Ctor && Component._Ctor.options) {
		Component._Ctor.options.data = Component.options.data;
	}
}
```

这个方法会在asyncData方法调用完毕后进行调用，可以看到，组件从asyncData方法中获取的数据会和组件原生的data方法获取的数据做一次合并，最终仍会在data方法中返回，所以得出，asyncData方法其实是原生data方法的扩展。

经过以上四步后，接下来就是渲染组件的工作了，整个过程可以用下图表示;

![http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHibpCia2R09xWDx7RcmVErAprwBicnTOyh5SAzdXawBjSuwzEg59e9ESvw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHibpCia2R09xWDx7RcmVErAprwBicnTOyh5SAzdXawBjSuwzEg59e9ESvw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

如上文所述，在.nuxt目录下，你可以找到server.js文件，这个文件封装了Nuxt.js在服务端渲染的逻辑，包括一个完整的Promise对象的链式调用，从而完成上面描述的整个服务端渲染的步骤。

## Nuxt的一些使用技巧
### nuxt.config.js的配置
nuxt.config.js是Nuxt.js的配置文件，可以通过针对一系列参数的设置来完成Nuxt.js项目的配置，可以在Nuxt.js官网(https://zh.nuxtjs.org/guide/configuration)找到针对这个文件的说明，下面举例一下常用的配置:

* head: 可以在这个配置项中配置全局的head，如定义网站的标题、meta，引入第三方的css，js等：
```js
head: {
	title: '百姓店铺',
	meta: [
		{ charset: 'utf-8' },
		{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
		{ name: 'applicable-device', content: 'pc,mobile' },
	],
	link: [
		{ rel: 'stylesheet', type: 'text/css', href: '...' },
	],
	script: [
		{ src: '...' }
	]
}
```

* build: 这个配置项用来配置Nuxt.js项目的构建规则，即webpack的构建配置，如通过vendor字段引入第三方模块，通过plugin字段配置webpack插件,通过loaders字段定义webpack加载器等。通常我们都会在build的vendor字段引入axios模块，从而在项目中进行HTTP请求(axios也是Vue.js官方推荐的HTTP请求框架)

```js
build: {
	vendor: ['core-js', 'axios'],
	loaders: [
		{
			test: /\.(scss|sass)$/,
			use: [{
				loader: 'style-loader',
			}, {
				loader: 'css-loader',
			}, {
				loader: 'sass-loader'
			}]
		}, {
			test: /\.(pnt|jpe?g|gif|svg)$/,
			loader: 'url-loader',
			query: {
				limit: 1000,
				name: 'img/[name].[hash:7].[ext]'
			}
		}, {
			test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
			loader: 'url-loader',
			query: {
				limit: 1000,
				name: 'fonts/[name].[hash:7].[ext]'
			}
		}
	]
}
```

* css: 在这个配置中，引入全局的css文件，之后每个页面都会被引用
* router: 可以在此配置路由的基本规则，以及进行中间件的配置。例如，你可以创建一个用来获取`User-Agent`的中间件，并在此加载。
* loading: Nuxt.js提供了一套页面内加载进度指示组件，可以在此配置颜色，禁用，或是配置自定义的加载组件。
* env: 可以在此配置用来在服务端和客户端共享的全局变量。

## 目录即路由
Nuxt.js在vue-router之上定义了一套自动化的生存规则，即依据pages的目录结构生成。例如，我们有以下目录结构:

![http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHEuyicmZfROJUYrtxQ2icKnAdKcLs5iaFnRCgibic7vcHrUXthayVdPCDU0g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHEuyicmZfROJUYrtxQ2icKnAdKcLs5iaFnRCgibic7vcHrUXthayVdPCDU0g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这个目录下含有一个基础路由(无参数)以及两个动态路由(带参数)，Nuxt.js会生成如下的路由配置表(可以在.nuxt目录下的router.js文件中找到):

```js
routes: [
	{
		path: '/',
		component: _abe13a78,
		name: 'index',
	}, {
		path: '/article/:id?',
		component: _48f202f2,
		name: 'article-id'
	}
];
```

对于article-id这个路由，路径中带有:id?参数，表明这是一个可选的路由，如果要将其设为必选，则必须在article目录下添加index.vue文件。

再看下面一个例子:

![http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHS9cvI1ooicy9YiaVKdWZ2gMgNZu4miaX0eDqrYQdia9GNDCjxbNib12pzXg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](http://mmbiz.qpic.cn/mmbiz_png/tuz2yibAYVszkMZt3UQ94Kl4AP7S5mXVHS9cvI1ooicy9YiaVKdWZ2gMgNZu4miaX0eDqrYQdia9GNDCjxbNib12pzXg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

由于有同名文件和文件夹的存在，在Nuxt.js会为我们生成嵌套路由，生成的路由结构如下，在使用时，需要增加<nuxt-child />标签来显示子视图的内容。

```js
routes: [
	{
		path: '/article',
		component: _f930b330,
		children: [
			{
				path: '',
				component: _143434a,
				name: 'article',
			},
			{
				path: ':id',
				component: ...,
				name: 'article-id'
			}
		]
	}
]
```

此外，Nuxt.js还可以设置动态嵌套路由。
