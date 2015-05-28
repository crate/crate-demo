/**
 * Responsible for sending/retrieving/checking blob's in the DB
 */
var Http = require('http');
var Blob = {};


/*
 * Put a blob
 */
Blob.put = function Put(table, hash, buffer, callback) {
    var node = this.node();
    var options = {
        method: 'PUT',
        path:   '/_blobs/' + table + '/' + hash,
        host:   node.host || 'localhost',
        port:   node.port || 4200,
    }

    var request = Http.request(options);

    request.write( buffer );
    request.end();

    if(typeof callback === 'function') {
        request.on('response', function(res) {
            if(res.statusCode !== 201) {
                callback(res.statusCode, null);
            }
            else {
                callback(null, hash);
            }
        });
    }

    return this;
}


/**
 * Get a blob
 */
Blob.get = function Get(table, hash, callback, location) {
    var options;

    if(location) {
        //location is sent when we get a 307 response, so i loop :)
        options = {
            method: 'GET',
            path:   location,
        };
    }
    else {
        var node = this.node();
        options = {
            method: 'GET',
            path:   '/_blobs/' + table + '/' + hash,
            host:   node.host || 'localhost',
            port:   node.port || 4200,
        };
    }

    var request = Http.request(options);

    request.end();

    if(typeof callback === 'function') {
        request.on('response', function(res) {
            if(res.statusCode == 200) {
                var buf = '';

                res.on('data', function(data) {
                    buf += data;
                });

                res.on('end', function() {
                    callback(null, buf);
                });
            }
            else if(res.statusCode == 307) {
                Blob.get(table, hash, callback, res.headers.location);
            }
            else {
                callback(null, hash);
            }
        });
    }

    return this;
}


/**
 * Check a blob
 */
Blob.check = function Check(table, hash, callback) {
    var node = this.node();
    var options = {
        method: 'HEAD',
        path:   '/_blobs/' + table + '/' + hash,
        host:   node.host || 'localhost',
        port:   node.port || 4200,
    }

    var request = Http.request(options);

    request.end();

    if(typeof callback === 'function') {
        request.on('response', function(res) {
            if(res.statusCode !== 200) {
                callback(res.statusCode, null);
            }
            else {
                callback(null, hash);
            }
        });
    }

    return this;
}


/**
 * Delete a blob
 */
Blob.delete = function Delete(table, hash, callback) {
    var node = this.node();
    var options = {
        method: 'DELETE',
        path:   '/_blobs/' + table + '/' + hash,
        host:   node.host || 'localhost',
        port:   node.port || 4200,
    }

    var request = Http.request(options);

    request.end();

    if(typeof callback === 'function') {
        request.on('response', function(res) {
            if(res.statusCode !== 204) {
                callback(res.statusCode, null);
            }
            else {
                callback(null, hash);
            }
        });
    }

    return this;
}


/**
 * Exports
 */
module.exports = Blob;
