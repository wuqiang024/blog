<!--
 * @Author: your name
 * @Date: 2021-10-20 14:25:47
 * @LastEditTime: 2021-10-20 15:14:23
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /recoms-is-master/Users/wuqiang/workspace/blog/react-native/CocoaPods常见问题.md
-->
# CocoaPods常见问题
## pod install 时出现
```js
xcodeproj 'path/to/Project.xcodeproj'
Unable to find a specification for `xxxxx (~> 1.x.x)` depended upon by Podfile.
```

需要把当前Pod的目录清理一下就行了。在终端执行以下命令：

```js
pod repo remove master
pod setup
```
setup成功后执行install或update即可。


## 遇到pod install或者pod update长时间卡在Updating local specs repositories
常见的解决方式是跳过更新cocoapods的spec仓库

```js
pod install --verbose --no-repo-update
pod update --verbose --no-repo-update
```

## 解决代理产生的Failed to connect to 127.0.0.1 port 54517: Connection refused问题
Failed to open TCP connection to 127.0.0.1:54517 (Connection refused - connect(2) for "127.0.0.1" port 54517)
查询代理
```js
$ env|grep -I proxy

$ http_proxy=127.0.0.1:54517
$ https_proxy=127.0.0.1:54517
```

取消代理
```js
$ unset http_proxy
$ unset https_proxy
$ env|grep -I proxy
```
未输出任何结果

然后再尝试`pod install`

## 升级CocoaPods，遇到CDN:trunk报错
解决方案:
1、podfile文件中指定source源为master：在podfile顶部加入`source 'https://github.com/CocoaPods/Specs.git'`,podfile中一定要指定master源，因为现在默认是trunk源
2、然后执行
```js
pod repo list // 查看一下源列表
pod repo remove trunk // 移除trunk源
```

## CocoaPods could not find compatible versions for pod "MJRefresh": In snapshot (Podfile.lock)

问题:报错
```js
You have either:
 * out-of-date source repos which you can update with `pod repo update` or with `pod install --repo-update`.
 * mistyped the name or version.
 * not added the source repo that hosts the Podspec to your Podfile.
```

解决方案:
1、把Podfile.lock文件删除，重新pod install即可
2、如果还不行把.xcworkspace也删了。

## xcrun unable to find simctl 
打开xcode，点击Xcode里头的`preferences > Locations`, 更改一下 Command Line Tools选项就可以了