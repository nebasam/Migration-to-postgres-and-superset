
{{ config(materialized='table') }}

select {{ref('station_summary')}}.flow_99,
       {{ref('station_summary')}}.flow_max,
       {{ref('station_summary')}}.flow_median,
       {{ref('station_summary')}}.flow_total,
       {{ref('station_summary')}}.n_obs,
       {{ref('station_metadata')}}.*
from {{ref('station_summary')}} 
inner join {{ref('station_metadata')}} 
on {{ref('station_summary')}}.ID = {{ref('station_metadata')}}.ID 