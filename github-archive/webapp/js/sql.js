;(function($){

    var SQL_ENDPOINT = 'http://' + window.location.hostname + ':4200/_sql';

    var SQLQuery = function SQLQuery(stmt, response, error) {
      this.stmt = stmt;
      this.rows = [];
      this.cols = [];
      this.rowCount = 0;
      this.duration = 0;
      this.error = error;
      this.failed = false;

      if (!this.error && response) {
        this.rows = response.rows;
        this.cols = response.cols;
        this.rowCount = response.rowcount;
        this.duration = response.duration;
      } else {
        this.failed = true;
      }
    }

    SQLQuery.prototype.toObjectArray = function() {
      var cols = this.cols;
      return this.rows.map(function(obj, idx){
        return SQLQuery.toObject(cols, obj);
      });
    };

    SQLQuery.toObject = function(headers, row) {
      if (headers.length != row.length) return {};
      var obj = {};
      for (var i=0; i<headers.length; i++) {
        obj[headers[i]] = row[i];
      }
      return obj;
    };

    SQLQuery.execute = function(stmt, args) {
      if (typeof stmt == 'undefined') throw new Error('Argument required: stmt');

      var data = {'stmt': stmt};
      if (typeof args != 'undefined') {
        data.args = args;
      }

      var deferred = $.Deferred();
      var promise = deferred.promise();
      promise.error = promise.fail;
      promise.success = promise.done;

      $.post(SQL_ENDPOINT, JSON.stringify(data)).done(function(data, xhr) {
          deferred.resolve(new SQLQuery(stmt, data, null));
        }).fail(function(xhr, status, message) {
          var data = xhr.responseJSON;
          var error = null;
          if (xhr.status >= 400 && data && data.error) {
            error = new Error(data.error.message);
            error.status = data.error.code;
          } else if (xhr.status >= 400) {
            error = new Error(message);
            error.status = xhr.status;
          } else if (xhr.status === 0) {
            error = new Error('Connection refused');
            error.status = xhr.status;
          }
          deferred.reject(new SQLQuery(stmt, data, error));
        }).always(function(response){
          console.info('SQLQuery: "' + stmt + '"', response);
        });

      return promise;
    };

    // expose on global window object
    window.SQLQuery = SQLQuery;

}(jQuery));

