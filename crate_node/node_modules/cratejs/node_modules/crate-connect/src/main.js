/**
 * Libs
 */
var Connect = require('./connect');
var Query   = require('./query');
var Execute = require('./execute');
var Blob    = require('./blob');


/**
 * Controller
 */
function Control(conf) {
	if(typeof conf === 'undefined') {
		conf = {};
	}

	this._connection = new Connect(conf);

	return this;
};


/**
 * Methods
 */
Control.prototype.Query   = Query;
Control.prototype.execute = Execute.direct; //Direct execution of a query
Control.prototype.blob    = Blob;


/**
 * Exports
 */
module.exports = Control;
