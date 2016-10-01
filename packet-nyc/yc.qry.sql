copy "nyc-yellowcab" from 's3://crate.sampledata/nyc.yellowcab/yc.2014.01.gz' with (compression='gzip');

--
select pickup_longitude , pickup_latitude , count(*) as c from "nyc-yellowcab" group by 1,2 having count(*) > 100 order by c desc limit 100;

select avg(tip_amount) from "nyc-yellowcab" where tip_amount > 0 limit 100;

select count(*), vendorid from "nyc-yellowcab" group by vendorid;

select avg(tip_amount), vendorid from "nyc-yellowcab" where tip_amount > 0 group by 2 limit 100;

select avg(cast(passenger_count as integer)) from "nyc-yellowcab";

select passenger_count, avg(tip_amount) from "nyc-yellowcab" where tip_amount > 0 group by passenger_count order by 1;

select passenger_count, count(*) from "nyc-yellowcab" group by passenger_count order by 1;
