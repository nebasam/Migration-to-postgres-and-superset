
    
    

select
    ID as unique_field,
    count(*) as n_records

from "tech_stack"."dbt"."station_metadata"
where ID is not null
group by ID
having count(*) > 1


