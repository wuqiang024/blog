```js
const express = require('express');
const path = require('path');
const redis = require('redis');

const db = redis.createClient();
const app = express();

app.use(express.static(path.join(__dirname, 'public')));

db.sadd('ferret', 'tobi');
db.sadd('ferret', 'loki');
db.sadd('cat', 'many');
db.sadd('cat', 'luna');

app.get('/search/:query?', function(req, res) {
    var query = req.params.query;
    db.smembers(query, function(err, vals) {
        if(err) return res.send(500);
        res.send(vals);
    })
})

app.get('/client.js', function(req, res) {
    res.sendFile(path.join(__dirname, 'client.js'));
})

if(!module.parent) {
    app.listen(3000);
}
```