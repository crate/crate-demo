copy uservisits
  from 's3://crate.amplab/data/5nodes/uservisits/part-*'
  with (bulk_size = 1000, compression = 'gzip', shared = true);
