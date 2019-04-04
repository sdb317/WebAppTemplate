do $$
begin
    if not exists (select 1 from pg_type where typname = 'demo_link_type') then
        create type demo_link_type
        as
            (
            entity_id integer,
            link_id integer,
            link_type integer
            );
    end if;
end$$;

/*

create or replace function
demo_test

    (
    test_link demo_link_type
    )
returns setof demo_link_type as $$
    select test_link as result;
$$ language sql;

select
    demo_test
        (
        row(1,2,3)
        );

create or replace function
demo_test_array
    (
    test_link_array demo_link_type[]
    )
returns setof demo_link_type as $$
    select * from unnest(test_link_array);
$$ language sql;

select
    demo_test_array
        (
        array[row(1,2,3),row(4,5,6)]::demo_link_type[]
        );

*/
