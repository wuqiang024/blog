Node.js的项目，都会依赖第三方模块。
在开发过程中，可能使用了某个模块，而后来的环节可能又不再使用。
而每次`npm install`一次，都会在node_modules中存留文件，时间一长，node_modules目录就变得臃肿起来。

有一种方法，仅一条命令:
```sh
npm prune
```

命令原理:
`npm prune命令的功能是根据package.json里的依赖项，删除不再需要的文件。