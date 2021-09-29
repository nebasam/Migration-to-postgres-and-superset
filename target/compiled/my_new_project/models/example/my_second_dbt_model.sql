-- Use the `ref` function to select from other models

select *
from "tech_stack"."dbt"."my_first_dbt_model"
where id = 1