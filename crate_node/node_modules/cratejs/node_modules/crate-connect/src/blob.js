/**
 * This is a helper for managing blobs
 * For now, this will simply expose a public method for managing blob's throught the connect.blob.js
 * In future versions i will extend this
 */
function Blob() {
    return {
        put: this._connection.blobPut.bind(this._connection),
        get: this._connection.blobGet.bind(this._connection),
        check: this._connection.blobCheck.bind(this._connection),
        delete: this._connection.blobDelete.bind(this._connection),
    };
}


/**
 * Exports
 */
module.exports = Blob;
