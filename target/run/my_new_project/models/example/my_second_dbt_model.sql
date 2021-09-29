
  create view "tech_stack"."dbt"."my_second_dbt_model__dbt_tmp" as (
    -- Use the `ref` function to select from other models

select *
from "tech_stack"."dbt"."my_first_dbt_model"
where id = 1
  );
