```js
const express = require('express');
const logger = require('morgan');
const vhost = require('vhost');

const main = express();

if(!module.parent) main.use(logger('dev'));

main.get('/', function(req, res) {
    res.send('hello from main app')
})

main.get('/:sub', function(req, res) {
    res.send('requested ' + req.params.sub);
});

const redirect = express();

redirect.use(function(req, res) {
    if(!module.parent) console.log(req.vhost);
    res.redirect('http://example.com:3000/' + req.vhost[0]);
});

const app = module.exports = express();

app.use(vhost('*.example.com), redirect);
app.use(vhost('example.com'), main);

if(!module.parent) {
    app.listen(3000);
}