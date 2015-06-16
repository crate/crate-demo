/**
 * Dependencies
 */
var Http  = require('http');
var Query = require('./connect.query');
var Blob  = require('./connect.blob');


/**
 * Connect
 */
var Connect = function Contructor(conf) {
	this.host = conf.host || 'localhost';
	this.port = conf.port || 4200;
	this.user = conf.user || null;
	this.pass = conf.pass || null;
	this.cluster = conf.cluster || [];

	if(this.cluster.length > 0) { //They sent an array with the host/port of each cluster
		this.lb_count = 0;
	}

	//TODO test connection method

	return this;
}


/**
 * Return node to send query
 */
Connect.prototype.node = function Node() {
    if(this.cluster.length > 0) {
        if(this.lb_count >= this.cluster.length) {
            this.lb_count = 0;
        }

        return this.cluster[ this.lb_count++ ];
    }
    else {
        return {
            host: this.host,
            port: this.port,
        }
    }
}


/**
 * Prototypes
 */
Connect.prototype.queryPost = Query.send;
Connect.prototype.blobPut   = Blob.put;
Connect.prototype.blobGet   = Blob.get;
Connect.prototype.blobCheck = Blob.check;
Connect.prototype.blobDelete = Blob.delete;


/**
 * Exports
 */
module.exports = Connect;
