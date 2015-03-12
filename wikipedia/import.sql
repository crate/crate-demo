-- dbext:type=CRATE:host=nuc1.p.fir.io:port=4200

alter table wikipedia set (refresh_interval = 0);
copy wikipedia from '/tmp/wikipedia/*';
alter table wikipedia set (refresh_interval = 1000);
