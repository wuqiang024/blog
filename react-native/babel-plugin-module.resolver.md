# babel-plugin-module-resolver 模块解析插件
***
babel-plugin-module-resolver 是一个babel模块解析插件,在.babelrc中可以配置模块的导入搜索路径，为模块添加一个新的解析器。这个插件允许你添加新的'根目录'，为模块添加一个新的解析器。这个插件允许你添加新的`根目录`，这些目录包含你的模块。它还允许你设置一个自定义别名目录，具体的文件，甚至其他NPM模块。

## 使用方法：
`npm install --save-dev babel-plugin-module-resolver`
然后配置项目根目录的`.babelrc`文件或者`babel.config.js`

```js
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./'],
        alias: {
          // folder
          '@components': './src/components',
          '@config': './src/config',
          '@constants': './src/constants',
          '@images': './src/images',
          '@manager': './src/manager',
          '@native': './src/native',
          '@pages': './src/pages',
          '@routers': './src/routers',
          '@themes': './src/themes',
          '@utils': './src/utils',
          '@redux': './src/redux',
          // common
          '@serverUtils': './src/utils/ServerUtils',
          '@navigation': './src/utils/NavigationService',
        },
      },
      ...prodPlugins,
    ],
  ],
};
```

## 选项
***
`root`: 一个字符串或根目录的数组，指定路径或全局路径(例如 ./src/**/components)
`alias`: 别名的配置，也可以使用别名node_modules依赖关系，而不仅仅是本地文件
`extensions`: 解析器中使用的扩展数组。覆盖默认扩展名(['.js', '.jsx', '.es', '.es6', '.mjs'])
`cwd`: 默认情况下，工作目录是用于解析器的工作目录，但是您可以覆盖你的项目。

自定义值babelrc将使插件根据要解析的文件查找最接近的babelrc配置。
自定义值packagejson将使插件查找最接近package.json的文件解析。

transformFunctions：将会变换其第一个参数的函数和方法的数组。默认情况下，这些方法是：require，require.resolve，System.import，jest.genMockFromModule，jest.mock，jest.unmock，jest.doMock，jest.dontMock。

resolvePath(sourcePath, currentFile, opts)：为文件中的每个路径调用的函数。默认情况下，模块解析器使用一个内部函数，如下所示：import { resolvePath } from 'babel-plugin-module-resolver'。该opts参数是通过babel配置通过选择对象。

## 在react-native中使用，让package正确解决各平台的模块，你必须添加`ios.js`和`.android.js`扩展
```json
{
  "plugins": [
    ["module-resolver", {
      "root": ["./src"],
      "extensions": [".js", ".ios.js", ".android.js"]
    }]
  ]
}
```