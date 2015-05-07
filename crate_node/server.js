/**
* Created by chrisward on 24/03/15.
*/

var Crate = require('cratejs');

var db = module.exports = new Crate({
  host: '192.168.59.103',
  port: 4200,
  /* Optional manual clustering
  cluster: [
  {
  host: '192.168.0.100',
  port: 4200,
}
]
*/
});

var findTweets = db.Select('tweets')
.columns(['id', 'text'])
.limit(100)
.order('id', 'asc');

findTweets.run(function(err, res) {
  if (err) {
    console.log(err);
  }
  else {
    if (res) {
      console.log(res);
    }
  }
});
