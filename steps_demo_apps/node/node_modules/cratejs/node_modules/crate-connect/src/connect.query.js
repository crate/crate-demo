/**
 * Responsible for sending query requests
 */
var Http = require('http');
var Query = {};


/**
 * Send a query POST
 */
Query.send = function Send(query, statements, callback) {
    var node = this.node();
	var options = {
		method: 'POST',
		path:   '/_sql',
        host:   node.host || 'localhost',
        port:   node.port || 4200,
		//No need to specify Keep-Alive, node will use the default global agent
	}

	var request = Http.request(options);

	//I really hope this query is sanatized!
	var data = {
		stmt: query
	}

	if(statements.length > 0) {
		data.args = statements;
	}

	request.write( JSON.stringify(data) );
	request.end();

	if(typeof callback === 'function') {
		request.on('response', function(res) {
			var buf = '';

			res.on('data', function(data) {
				buf += data;
			});

			res.on('end', function() {
                var result = JSON.parse(buf);

                if(result.error) {
                    callback(result.error, null);
                }
                else {
                    callback(null, result);
                }
			});
		});
	}

	return this;
}


/**
 * Exports
 */
module.exports = Query;
