```javascript
var express = require('express');
var app = express();
app.engin('html', require('ejs').renderFile());
app.set('views', path.join(__dirname, 'views'));
app.set('view engin', 'html');
```