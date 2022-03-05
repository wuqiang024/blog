/*
 * @Author: your name
 * @Date: 2022-02-25 23:35:14
 * @LastEditTime: 2022-02-25 23:42:37
 * @LastEditors: your name
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/node/test.js
 */
const EventEmitter = require('events');
const emitter = new EventEmitter();
emitter.on('test', function(param) {
  console.log('test', param)
})
emitter.emit('test', 'name');