copy uservisits
  from 's3://crate.amplab/data/tiny/uservisits/part-*'
  with (bulk_size = 1000, compression = 'gzip', shared = true);
