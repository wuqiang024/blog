<!--
 * @Author: your name
 * @Date: 2021-09-29 15:47:20
 * @LastEditTime: 2021-09-29 16:15:37
 * @LastEditors: your name
 * @Description: In User Settings Edit
 * @FilePath: /blog/react/react路由中统一处理title.md
-->
# react路由中统一处理title.md
***
react想在每个页面设置不同的title, 可以在每个页面的`componentDidMount()`钩子中设置`document.title=xx`来设置标题，但是这样太麻烦，更方便的方式是在index.js入口处统一设置`document.title=title`。

`routes.js`
```js
import Index from './pages/index';
let routes = [
  {
    path: '/index',
    component: Index,
    meta: {
      title: '首页'
    }
  }
];

export default routes;
```

`index.js`入口页面
```js
import React from 'react';
import ReactDom from 'react-dom';
import routes from './routes';
import {HashRouter, Route, Switch, Redirect} from 'react-router-dom'
import App from './App';
import {Provider} from 'react-redux';

ReactDom.render(
  <Provider store={store}>
    <HashRouter>
      <App>
        <Switch>
        </Switch>
      </App>
  </Provider>
)
```