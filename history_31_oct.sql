select distinct(csymbol),high,low,diff,qstart,qend from quarter where csymbol='HDFCBANK' order by qstart desc;
select distinct(csymbol),high,low,diff,qstart,qend from quarter where csymbol='SUNPHARMA' order by qstart desc;
select distinct(csymbol),diff,(((diff)/(select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart))*100)as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),high,low,diff,qstart,qend from quarter where csymbol='HDFCBANK' order by csymbol, diff desc;
select high,low,distinct(csymbol),diff,qstart,qend from quarter where csymbol='HDFCBANK' order by csymbol, diff desc;
select distinct(csymbol),diff,qstart,qend from quarter where csymbol='HDFCBANK' order by csymbol, diff desc;
select distinct(csymbol),diff,qstart,qend from quarter where symbol='HDFCBANK' order by csymbol, diff desc;
select distinct(csymbol),diff,qstart,qend from quarter order by csymbol, diff desc;
delete from quarter where qstart='2022-10-01';
select distinct(csymbol),diff,qstart from quarter q where q.qstart='2022-10-01'  and diff >= (select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart);
delete from quarter where qstart='2022-10-28';
select distinct(csymbol),diff,(((select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)/diff)*100)as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,(((diff/select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart))*100)as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)/diff) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)/diff)) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)/diff)*100) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((diff/(select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)*100) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,((diff/select max(diff) from quarter where csymbol=q.csymbol and qstart!=q.qstart)*100) as per,qstart from quarter q where q.qstart='2022-10-01';
select distinct(csymbol),diff,qstart from quarter q where q.qstart='2022-10-01'