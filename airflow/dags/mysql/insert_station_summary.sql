LOAD DATA 
INFILE '~/Downloads/station_summary.csv' 
INTO TABLE Station_Summary 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n';