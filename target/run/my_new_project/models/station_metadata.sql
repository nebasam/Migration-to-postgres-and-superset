

  create  table "tech_stack"."dbt"."station_metadata__dbt_tmp"
  as (
    

SELECT ID, FWY, DIR, District, County, City, State_PM, Abs_PM, Latitude, Longitude, Length, Type, Lanes, Name
FROM analytics.I80Stations
  );