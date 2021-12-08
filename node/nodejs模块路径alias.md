# nodejs模块路径alias
***
nodejs的模块引用，使用相对路径，会写一堆`../`，相当不方便。
有两种好的修改方式:
1、NODE_PATH设置路径别名
```json
"scripts": {
  "start": "cross-env NODE_PATH=.;./mode node index.js",
}
```
NODE_PATH的路径用分号或冒号分割多个路径，`.`表示本目录,`./mode`表示一个子目录。
缺点是不同系统设置多个路径的分隔符不同，用了cross-env也无济于事。

2、module_alias模块
```s
npm i --save module-alias
```

```json
"_moduleAliases": {
  "@root": ".", // Application root
  "@deep": "src/some/very/deep/directory/or/file",
  "@my_module": "lib/some-file.js",
  "something": "src/foo", // or without @. actually, it could be any string
}
```

这个模块可以在package.json中注册alias,跟webpack相似很好用。
其原理是，修改了nodejs的查找路径的方法Module._resolveFilename,先从alias中找，然后替换，再用原来的方法找。
修改了nodejs内部的Module._nodeModulePaths，使得_moduleDirectories中的目录可以实现类似node_modules的效果。