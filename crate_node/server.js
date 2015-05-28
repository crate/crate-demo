/**
* Created by chrisward on 24/03/15.
*/

var Crate = require('cratejs');

var db = module.exports = new Crate({
  host: 'st01p.aws.fir.io',
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

var findSteps = db.Select('steps')
.columns(['num_steps'])
.where({
  username: 'gosinski',
  month_partition: '201409'
})
.limit(100);

findSteps.run(function(err, res) {
  if (err) {
    console.log(err);
  }
  else {
    if (res) {
      console.log(res);
    }
  }
});

db.execute("SELECT date_trunc('day', ts), sum(num_steps) FROM steps WHERE username = ? AND month_partition = ? GROUP BY 1", ['gosinski', '201409'], function(err, res) {
  if (err) {
    console.log(err);
  }
  else {
    if (res) {
      console.log(res);
    }
  }
});
