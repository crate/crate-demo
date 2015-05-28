/**
* Execute a constructed db.Query()
*/
function Execute(statements, callback) {
	if(typeof statements === 'function') { //statements was sent as the callback
		callback = statements;
		statements = [];
	}

	this._connection.queryPost(this._queryString, statements || [], callback);
                        //this._queryString; Can be found on ./query.js constructor function
}


/**
 * Direct query execution
 */
Execute.direct = function Direct(query, statements, callback) {
	if(typeof statements === 'function') { //statements was sent as the callback
		callback = statements;
		statements = [];
	}

	this._connection.queryPost(query, statements || [], callback);
}


/**
* Exports
*/
module.exports = Execute;
