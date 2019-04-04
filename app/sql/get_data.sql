create or replace function
demo_get_data
	(
	_table_type anyelement,
	_criteria varchar(1024)

	)
returns setof anyelement 
as $$
declare SQL text;
begin
/*
A generic stored procedure to retrieve data from a single table, based on the specified criteria.
*/
	SQL:=
		'
		select
            *
		from
            '||pg_typeof(_table_type)||'
		where		
            '||_criteria||'
		';
	return query execute SQL;
end;
$$ language plpgsql;

/*
	select * from 
		demo_get_data
			(
			null::public.project_lifecycle_city,
			'country_id=10'
			);
*/

create or replace function
demo_get_data_json
	(
	_table varchar(64),
	_columns varchar(1024), /* Can be '*' for all columns */
	_criteria varchar(1024)

	)
returns setof json
as $$
declare SQL text;
begin
/*
A generic stored procedure to retrieve json data for specified columns from a single table, based on the specified criteria.
*/
	SQL:=
		'
		select
			array_to_json(array_agg(data))
		from
			(
			select
                '||_columns||'
			from
				demo_get_data
					(
					null::'||_table||',
					'''||_criteria||'''
					)
			) data
		';
	return query execute SQL;
end;
$$ language plpgsql;

/*
	select
		demo_get_data_json
			(
			'public.project_lifecycle_city',
            'name_native,country_id',
			'country_id=10'
			);
*/

create or replace function
demo_get_data_xml
	(
	_table varchar(64),
	_columns varchar(1024), /* Can be '*' for all columns */
	_criteria varchar(1024)

	)
returns xml
as $$
declare SQL text;
begin
/*
A generic stored procedure to retrieve json data for specified columns from a single table, based on the specified criteria.
*/
	SQL:=
		'
		select
			query_to_xml
				(
				select
					'||_columns||'
				from
					demo_get_data
						(
						null::'||_table||',
						'''||_criteria||'''
						)
				)
		';
	execute SQL;
end;
$$ language plpgsql;

/*
	select
		demo_get_data_xml
			(
			'public.project_lifecycle_city',
            'name_native,country_id',
			'country_id=10'
			);
*/

