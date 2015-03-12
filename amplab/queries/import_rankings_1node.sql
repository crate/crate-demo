copy rankings
  from 's3://crate.amplab/data/1node/rankings/part-*'
  with (bulk_size = 1000, compression = 'gzip', shared = true);
