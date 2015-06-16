crate-connect
=======
[![Build Status](https://travis-ci.org/herenow/crate-connect.svg?branch=master)](https://travis-ci.org/herenow/crate-connect)

A simple node.js driver to connect to a Crate.io Data Storage, this was originally part of the [CrateJS](https://github.com/herenow/cratejs) driver, now [CrateJS](https://github.com/herenow/cratejs) is an extension of crate-connect.


Installation
----------
```
npm install crate-connect
```


Sample usage
----------

```javascript
var Crate = require('crate-connect');

// You can have as many db instance as you please :)
// You should probably add this part to another module and export it!
var db = new Crate({
  host: 'localhost', //Defaults to localhost
  port: 4200, //Defaults to 4200
  // You can also send in a cluster of nodes
  cluster: [
      {
        host: 'localhost',
        port:4200
      },
  ]
});

// Now lets build some queries, using placeholders, you can either use ? or $1, $2, $3...
var q = {
  getSomeTweets: db.Query('SELECT text FROM tweets LIMIT ?'),
  getReTweeted:  db.Query('SELECT text FROM tweets WHERE retweeted = $1 LIMIT $2'),
};

// Get some tweets
q.getSomeTweets.execute([10], onResponse);

// Get only tweets with retweets
q.getReTweeted.execute([true, 10], onResponse);

function onResponse(err, res) {
    if(err) {
      //Do something
      return;
    }

    console.log('Returned %d rows', res.rowcount);
    console.log('Columns returned:\n', res.cols);
    console.log(res.rows);
}
```


Methods
----------

###db.Query(string)
* This constructs a query and returns an .execute() method.


###db.execute(query, statements, callback)
* This executes a query directly
* Statements is an optional parameter, you can replace it with the callback
```javascript
db.execute('SELECT * FROM tweets LIMIT ?', [1], function(err, res) {})
```


###db.blob()
* Methods related to managing blob's
* Note that this does not construct the sha1 hash from the buffer, you need to do it yourself.
* Note that if the sha1 hash is not correct, the blob wont be inserted. **The sha1 hash must be calculated from the blob to be inserted.**

####blob().put(table, sha1Hash, buffer, callback)
```javascript
var buffer = new Buffer('sample')
var hash = crypto.createHash('sha1').update(buffer).digest('hex')

####blob().put('imagesTable', hash, buffer, function(err) {
    if(err) {
        //err.statusCode
    }
})
```

####blob().get(table, sha1Hash, callback)
```javascript
db.blob().get('imagesTable', '8151325dcdbae9e0ff95f9f9658432dbedfdb209', function(err, buffer) {
    if(err) {
        //err.statusCode
    }
})
```

####blob().check(table, sha1Hash, callback)
```javascript
db.blob().check('imagesTable', '8151325dcdbae9e0ff95f9f9658432dbedfdb209', function(err) {
    if(err) {
        //err.statusCode
    }
})
```

####blob().delete(table, sha1Hash, callback)
```javascript
db.blob().check('imagesTable', '8151325dcdbae9e0ff95f9f9658432dbedfdb209', function(err) {
    if(err) {
        //err.statusCode
    }
})
```


TODO
---------
* Refactor some pieces of this code, its messy :(


Contributors
---------
- [herenow](https://github.com/herenow)
