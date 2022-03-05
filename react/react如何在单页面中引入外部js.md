<!--
 * @Author: your name
 * @Date: 2021-12-17 18:55:02
 * @LastEditTime: 2021-12-17 18:57:48
 * @LastEditors: your name
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/react/react如何在单页面中引入外部js.md
-->
# react如何在单页面中引入外部js
***
如果不想在全部页面中引入html，只想在某个组件中引入

## 1、可以动态的写一个加载js的函数，实现加载

## 2、使用插件 react-load-script，如果没有安装可以使用 yarn add react-load-script 或者 npm install react-load-script，看你使用哪个包管理工具。
```js
import React from 'react';
import Script from 'react-load-script';

class DynamicScriptExample extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scriptStatus: 'no'
        }
    }

    handleScriptCreate() {
      this.setState({ scriptLoaded: false })
    }
     
    handleScriptError() {
      this.setState({ scriptError: true })
    }
     
    handleScriptLoad() {
      this.setState({ scriptLoaded: true, scriptStatus: 'yes' })
    }

    render() {
        return (
            <>
            <Script
              url="https://cdn.staticfile.org/jquery/3.3.1/jquery.min.js"
              onCreate={this.handleScriptCreate.bind(this)}
              onError={this.handleScriptError.bind(this)}
              onLoad={this.handleScriptLoad.bind(this)}
            />
            <div>动态脚本引入状态：{this.state.scriptStatus}</div>
            </>
        );
    }
}

export default DynamicScriptExample;
```

## 3、createObjectUrl