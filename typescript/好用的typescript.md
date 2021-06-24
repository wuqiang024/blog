# TS中的枚举定字符串
* 通过给枚举定义字符串可以使用消息管理器
* 之前都是用静态对象定义

```js
import { EventEmitter } from 'events';

enum EventType {
    OPEN = 'open',
    CLOSE = 'close',
}

const eventEmitter = new EventEmitter();

eventEmitter.on(EventType.OPEN, () => {
    console.log('call open');
})

eventEmitter.on(EventType.CLOSE, () => {
    console.log('call close');
})

eventEmitter.emit(EventType.OPEN);
eventEmitter.emit(ventType,CLOSE);
```

# TS中的单例模式

```js
export class Singleton {
    private static _instance: Singleton
    private constructor() {}
    static getInstance(): Singleton {
        if(!Singleton._instance) {
            Singleton._instance = new Singleton()
        }
        return Singleton._instance
    }
}
```

# TS中的Setter和getter实现

```js
private _name: string;
set name(val: string) {
    this._name = val
}

get name() {
    return this._name
}
```