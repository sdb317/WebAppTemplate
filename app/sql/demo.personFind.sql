create or replace function
demo_find_person
	(
	_criteria varchar(256),
    _detail boolean,
    _audit boolean
	)
returns setof json
as $$
declare SQL text; 
declare table_list text; 
declare column_list text; 
begin
	 /*  */
	if _detail then
	    table_list:=
		    '
			public.demo_person person
		    ';
	    column_list:=
		    '
			person.id,
			person.first_name,
			person.last_name,
            person.email,
            person.type,
            person.saved_by,
            person.saved_on,
			(
			select
				coalesce(array_to_json(array_agg(row_to_json(link_results))),''[]'')
			from
				(
				select
                    case
                        when link.link_type=(select numeric from public.plus__definition where category=''EntityType'' and label=''<OtherEntity>'')
                            then (select abbreviation from public.project_lifecycle_consortium where id=link.link_id)
                        else ''''
                    end as name,
                    link.link_id as value,
                    link.link_type as type
				from
					public.plus__link link
				where
					link.entity_id=person.id
                    and
                    link.entity_type=(select numeric from public.demo__definition where category=''EntityType'' and label=''Person'')
				) link_results
			) as links
		    ';
	else
	    table_list:=
		    '
            public.plus_person person
            left outer join public.plus_person_audit person_audit
                on person_audit.person_id=person.id
		    ';
	    column_list:=
		    '
			person.id,
			person.first_name,
			person.last_name
		    ';
	end if;
	if _audit then
	    column_list:=column_list ||
		    '
			,
			(
			select
				coalesce(array_to_json(array_agg(row_to_json(audit_results))),''[]'')
			from
				(
				select
			        person_audit.id,
			        person_audit.person_id,
					person_audit.first_name,
					person_audit.last_name,
					person_audit.email,
					person_audit.type,
                    person_audit.saved_by,
                    person_audit.saved_on
				from
					public.demo_person_audit person_audit
				where
					person_audit.person_id=person.id
				order by
					person_audit.id desc
				) audit_results
			) as audits
		    ';
	end if;
	SQL:=
		'
		select 
			array_to_json(array_agg(person.* order by person.person_date desc))
		from
			(
			select 
		' 
		|| column_list ||
		'
			from 
		' 
		|| table_list ||
		'
			where 
		' 
		|| _criteria ||
		'
		group by 
			person.id
			) person
		';
	return query execute SQL;
end;
$$ language plpgsql;

/*
	select 
		demo_find_person 
			( 'true', true, true ); 
*/

