

select "tech_stack"."dbt"."station_summary".flow_99,
       "tech_stack"."dbt"."station_summary".flow_max,
       "tech_stack"."dbt"."station_summary".flow_median,
       "tech_stack"."dbt"."station_summary".flow_total,
       "tech_stack"."dbt"."station_summary".n_obs,
       "tech_stack"."dbt"."station_metadata".*
from "tech_stack"."dbt"."station_summary" 
inner join "tech_stack"."dbt"."station_metadata" 
on "tech_stack"."dbt"."station_summary".ID = "tech_stack"."dbt"."station_metadata".ID