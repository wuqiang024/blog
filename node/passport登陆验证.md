本项目主要使用了以下技术 node + express + sequelize + postgreSql + passport 

# 需要引入的插件

```sh
npm install passport passport-local express-session
```

# 配置passport
app.js添加

```js
const session = require('express-session');
app.use(session({
    secret: 'test',
    cookie: { httpOnly: true, secure: false, maxAge: 30*24*60*60*1000}, //保存30天
    secure: true, // 如果是true需要https,如果不是则不需用。
    resave: false,
    saveUninitialized: false
}));

require('./config/passport')(app);
```

创建文件passport.js

```js
const User = require('../control/User');
const passport = require('passport');
const localStrategy = require('passport-local').Strategy;

module.exports = function(app) {
    app.use(passport.initialize());
    app.use(passport.session());

    var isValidPassword = function(user, password) {
        return user.password = password;
    }

    // 在调用req.login()后执行该方法，将用户的user.js保存到session中
    passport.serializeUser(function(user, done) {
        done(null, user.id);
    })

    passport.deserializeUser(function(id, done) {
        User.queryUserById(id).then((user) => {
            done(null, user);
        }).catch((err) => {
            done(err);
        })
    })
}
```

# 在登录中的路由中进行认证
routes/login.js

```js
const express = require('express');
const router = express.Router();
const login = require('../control/login');

router.post('/', (req, res, next) => {
    login(req).then((msg) => {
        res.send(msg);
    }).catch((err) => {
        res.send(err);
    })
})

module.exports = router;
```

control/login.js认证方法调用

```js
const passport = require('passport');
module.exports = function(req) {
    return new Promise((resolve, reject) => {
        passport.authenticate('login', function(err, user, info) {
            if(err || !user) {
                reject(info)
            } else {
                req.login(user, function(err) {
                    if(err) {
                        reject({message: '认证失败'})
                    } else {
                        delete user.dataValues['password']
                        resolve(user);
                    }
                })
            }
        })(req)
    })
}
```