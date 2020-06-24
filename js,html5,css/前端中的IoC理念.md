# 前端中的IOC理念
***

## 背景
***
前端应用在不断扩大的过程中，内部模块之间的依赖可能也会随之越来越复杂，模块之间的低复用性导致应用难以维护，不过我们可以借助计算机领域的一些优秀的编程理念来一定程度上解决这些问题，接下来讲述的IOC就是其中之一。

## 什么是IOC
***
IoC的全称叫做`Inversion of Control`，可翻译为控制反转或依赖倒置，他主要包括了三个原则。

1、高层次的模块不应该依赖于低层次的模块，他们都应该依赖于抽象
2、抽象不应该依赖于具体实现，具体实现应该依赖于抽象
3、面向接口编程，而不要面向实现编程

概念总是抽象的，所以下面将以一个例子来解释上述的概念:

假设需要构建一个应用叫APP，他包含一个路由模块Router和一个页面监控模块Track，一开始可能会这么实现。

```js
// app.js
import Router from './modules/Router';
import Track from './modules/Track';

class App {
    constructor(options) {
        this.options = options;
        this.router = new Router();
        this.track = new Track();

        this.init();
    }

    init() {
        window.addEventListener('DOMContentLoaded', ()=> {
            this.router.to('home');
            this.track.tracking();
            this.options.onReady();
        })
    }
}

// index.js
import App from 'path/to/App';
new App({ onReady() {} });
```

看起来没什么问题，但是实际应用中需求是非常多变的，可能需要给路由新增功能(比如实现history模式)或者更新配置(启用history, new Router({mode: 'history'}));这就不得不在App内部去修改这个模块。那么如何解决这个问题呢，解决方案就是接下来要讲述的依赖注入(Dependency Injection)。

## 依赖注入
***
所谓的依赖注入，简单来说就是把高层模块所依赖的模块通过传参的方式把依赖注入到模块内部，上面的代码可以通过依赖注入的方式改造成如下方式。

```js
// app.js
class App {
    constructor(options) {
        this.options = options;
        this.router = options.router;
        this.track = options.track;

        this.init()
    }

    init() {
        window.addEventListener('DOMContentLoaded', () => {
            this.router.to('home');
            this.track.tracking();
            this.options.onReady();
        })
    }
}

// index.js
import App from 'path/to/App';
import Router from './modules/Router';
import Track from './modules/Track';

new App({
    router: new Router(),
    track: new Track(),
    onReady() {}
})
```

可以看到，通过依赖注入解决了上面所说的`INNER BREAKING`问题，可以直接在App外部对各个模块进行修改而不影响内部。

是不是就万事大吉了？理想很丰满，现实很骨感，没过两天产品就给你提了一个新需求，给APP增加一个分享模块Share。这样的话又回到了上面所提到的`INNER BREAKING`的问题上，你不得不对App模块进行修改加上一行this.share = options.share,这明显不是我们期望的。

虽然App通过依赖注入的方式在一定程度上解耦了与其他几个模块的依赖关系，但是还是不够彻底，其中的this.router和this.track等属性其实都还是对具体实现的依赖，明显违背了IoC思想的准则，那如何进一步抽象App呢。

```js
class App {
    static modules = [];
    constructor(options) {
        this.options = options;
        this.init()
    }

    init() {
        window.addEventListener('DOMContentLoaded', () => {
            this.initModules();
            this.options.onReady(this);
        })
    }

    static use(module) {
        Array.isArray(module) ? module.map(item => App.use(item) : App.modules.push(module))
    }

    initModules() {
        App.modules.map(module => module.init && typeof module.init == function && module.init(this));
    }
}
```

经过改造后，App内部已经没有具体实现的代码了，看不到任何业务代码了，那么如何使用App来管理我们的依赖呢。

```js
// modules/Router.js
import Router from 'path/to/Router';
export default {
    init(app) {
        app.router = new Router(app.options.router);
        app.router.to('home');
    }
}

// modules/Track.js
import Track from 'modules/Track.js';
export default {
    init(app) {
        app.track = new Track(app.options.track);
        app.track.tracking();
    }
}

// index.js
import App from 'path/to/App';
import Router from './modules/Router';
import Track from './modules/Track';

App.use([Router, Track]);

new App({
    router: { mode: 'history' },
    track: {},
    onReady(app) {}
})
```

可以发现App模块在使用上也非常的方便，通过App.use()方法来注入依赖，在`./modules/some-module.js`中按照一定的约定去初始化相关配置，比如此时需要新增一个Share模块的话，无需到App内部去修改内容。

```js
import Share from 'path/to/Share';
export default {
    init(app) {
        app.share = new Share();
        app.setShare = data => app.share.setShare(data);
    }
}

// index.js
App.use(Share);
new App({
    onReady(app) {
        app.setShare({ title: '', description: '' })
    }
});
```

直接在App外部去use这个Share模块即可，对模块的注入和配置极为方便。

那么在App内部到底做了哪些工作呢，首先从App.use方法说起。

```js
class App {
    static modules = [];
    static use(module) {
        Array.isArray(module) ? module.map(item => App.use(item) : App.modules.push(module))
    }
}
```

可以很清楚的发现，App.use做了一件非常简单的事情，就是把依赖保存在了App.modules属性中，等待后续初始化模块的时候调用。

接下来我们看一下模块初始化方法`this.initModules()`具体做了什么事情。

```js
class App {
    initModules() {
        App.modules.map(module => module.init && typeof module.init == 'function' && module.init(this));
    }
}
```

可以发现该方法同样做了一件非常简单的事情，就是遍历App.modules中所有的模块，判断模块是否包含init属性并且该属性必须为一个函数，如果判断通过的话，该方法就会去执行模块的init方法并把App的实例this传入其中，以便在模块中引用他。

从这个方法可以看出，要实现一个可以被App.use()的模块，就必须满足两个约定:

1、模块必须包含init属性
2、init必须是一个函数

这其实就是IoC思想中面对接口编程而不是面对实现编程的很好的体现。App不关心模块具体实现了什么，只要满足对接口init的约定就可以了。

此时回去看Router的模块的实现就可以很容易理解为什么要这么写了。

```js
// modules/Router
import Router from 'path/to/Router';
export default {
    init(app) {
        app.router = new Router(app.options.router);
        app.router.to('home');
    }
}
```

## App模块此时应该称之为容器比较合适了，跟业务已经没有任何关系了，他仅仅只是提供了一些方法来辅助管理注入的依赖和控制模块如何执行。

控制反转(Inversion of Control)是一种思想，依赖注入则是这一思想的一种具体实现方式，而这里的App则是辅助依赖管理的一个容器。