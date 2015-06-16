var assert = require('assert');

var Crate, db, query;

describe('Cratejs', function() {

	describe('Try to initiate a CrateJS client', function(){
		it('Should initiate a CreateJS client', function() {
	            Crate = require('../index.js');
		    db = new Crate({
				host: process.env.CRATE_TEST_HOST || '127.0.0.1',
				port: process.env.CRATE_TEST_PORT || 4200,
			});
		});
	});

	describe('Build some queries', function(){
		it('Should build some queries', function() {
            query = [
                db.Query('SELECT * FROM sys.cluster LIMIT ?')
            ];
		});
	});

	describe('Now try to query the dabtase', function(){
		it('Should return an rows from the query', function(done) {
			query[0].execute([100], function(err, res) {
				if(err) {
					return done(err);
				}
				else if(res.rowcount < 1) {
					return done('no rows returned');
				}
				done();
			});
		});
        it('Should return an rows from the query (direct execution)', function(done) {
            db.execute('SELECT * FROM sys.cluster LIMIT ?', [100], function(err, res) {
                if(err) {
                    return done(err);
                }
                else if(res.rowcount < 1) {
                    return done('no rows returned');
                }
                done();
            });
        });
	});

	describe('Blobs', function() {
		it('Create sample blob table, this command should not fail, execute() was already tested', function(done) {
			db.execute('CREATE BLOB TABLE blob_sample', function() {
				done()
			})
		})
		it('Should put a blob in the table', function(done) {
			db.blob().put('blob_sample', '4f041e948dfaae599ae3f5c89f5ae698ffec4b38', new Buffer("Lorem ipsum?"), function(err) {
				if(err && err !== 409) {
					//Ignore error 409, because 409 is a conlifct error, blob already exists
					return done(err);
				}
				done()
			})
		})
		it('Should check a blob in the table', function(done) {
			db.blob().check('blob_sample', '4f041e948dfaae599ae3f5c89f5ae698ffec4b38', function(err, buffer) {
				if(err) {
					return done(err);
				}
				done()
			})
		})
		it('Should get a blob from the table', function(done) {
			db.blob().get('blob_sample', '4f041e948dfaae599ae3f5c89f5ae698ffec4b38', function(err, buffer) {
				if(err) {
					return done(err);
				}
				if(buffer != new Buffer("Lorem ipsum?")) {
					return done("The returned buffer was not the same as the one we sent it.")
				}
				done()
			})
		})
		it('Should delete a blob from the table', function(done) {
			db.blob().delete('blob_sample', '4f041e948dfaae599ae3f5c89f5ae698ffec4b38', function(err) {
				if(err) {
					return done(err);
				}
				done()
			})
		})
	})


});
