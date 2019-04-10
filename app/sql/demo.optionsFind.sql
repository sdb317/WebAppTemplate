create or replace function
demo_get_options
	(
	_category varchar(256),
	_item varchar(256)
	)
returns setof json
as $$
begin
    return query
    select 
        array_to_json(array_agg(definition order by definition.numeric)) 
    from 
        public.demo__definition definition 
    where 
        lower(definition.category)=lower('Option'||_category||_item);
end;
$$ language plpgsql;

/*

select
    demo_get_options
	    (
        'Project',
        'Phase'
	    )

*/
