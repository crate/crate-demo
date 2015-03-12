-- users
copy users from '/data/sampledata/users.json.gz' with (bulk_size=1000, compression='gzip');
-- refresh
refresh table users;


-- steps
copy steps from '/data/sampledata/steps_*.json.gz' with (bulk_size=1000, compression='gzip');
-- refresh
refresh table steps;

