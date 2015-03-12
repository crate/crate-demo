copy rankings
  from 's3://crate.amplab/data/tiny/rankings/part-*'
  with (bulk_size = 1000, compression = 'gzip', shared = true);
