<!--
 * @Author: your name
 * @Date: 2022-03-05 14:01:55
 * @LastEditTime: 2022-06-13 00:33:07
 * @LastEditors: wuqiang
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/git/无法通过用户名密码登录git.md
-->
# 无法通过用户名密码登录git了
***
Github在2021.8.13更新了密码验证方式，如果你还像之前一样进行git push，基本上会遇到一个报错：
```js
please use personal access token instead
```

## 参考
http://www.mac52ipod.cn/post/mac-keychain-access-helps-you-find-back-forgotten-password.php

## 第一步，在GitHub网站创建Personal Access Token
***
Settings=> Developer Settings => Personal Access Token => Generate New Token

note这里写上一个自定的名称

下面这个日期可以自行选择（但GitHub不建议选择永久）

之后的所有复选框可以都打勾

最后生成一个key

## 第二步 对于mac用户
***
如果你的电脑配置过git就省过第二步。
打开
`Finder > 应用程序 > 实用工具 > Keychain access（钥匙串访问）`这个应用，然后搜索：github.com

把类型为Internet password的这个删掉

## 第二步：对于windows用户
***
在控制面板中找到：凭据管理器（Credential Manager） =》 Windows Credentials=》搜索git:https://github.com =》 编辑=》将密码替换为GitHub生成的Personal Access Token

## 第三步：正常提交修改
***
把修改的内容进行git push后，一般会提示：
你需要分别输入用户名和那一串token密码，最后就可以正常提交了