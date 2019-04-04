create or replace function
demo_save_person
    (
    _saved_by varchar(256),
    _id int,
    _links demo_link_type[],
    _email varchar(256),
    _first_name varchar(256),
    _last_name varchar(256)
    )
returns int as
$$
begin
    if _id=0 then /* If it is new */
        insert into
            public.demo_person
                (
                uuid,
                saved_on,
                saved_by,
                email,
                first_name,
                last_name
                )
            values
                (
                (select md5(random()::text || clock_timestamp()::text)::uuid),
                now(),
                _saved_by,
                _email,
                _first_name,
                _last_name
                );
        _id=currval(pg_get_serial_sequence('demo_person','id')); /* Get the new identity value */
        insert into /* Add new links */
            public.demo__link
                (
                entity_type,
                entity_id,
                link_type,
                link_id
                )
            select
                (select numeric from public.demo__definition where category='EntityType' and label='Person'),
                _id, /* Override the value in the array argument, which will be 0 */
                new_link.link_type,
                new_link.link_id
            from
                unnest(_links) new_link;
    else
        insert into
            public.demo_person_audit
                (
                uuid,
                saved_on,
                saved_by,
                person_id,
                email,
                first_name,
                last_name
                )
            select
                uuid,
                saved_on,
                saved_by,
                id,
                email,
                first_name,
                last_name
            from
                public.demo_person
            where
                id=_id;
        update
            public.demo_person
                set
                    saved_on=now(),
                    saved_by=_saved_by,
                    email=_email,
                    first_name=_first_name,
                    last_name=_last_name
                where
                    id=_id;
        insert into /* Add new links */
            public.demo__link
                (
                entity_type,
                entity_id,
                link_type,
                link_id
                )
            select
                (select numeric from public.demo__definition where category='EntityType' and label='Person'),
                _id, /* Override the value in the array argument, which will be 0 */
                new_link.link_type,
                new_link.link_id
            from
                unnest(_links) new_link
                left outer join demo__link old_link
                    on
                        old_link.entity_type=(select numeric from public.demo__definition where category='EntityType' and label='Person')
                        and
                        old_link.entity_id=new_link.entity_id
                        and
                        old_link.link_type=new_link.link_type
                        and
                        old_link.link_id=new_link.link_id
            where
                old_link.entity_id is null; /* I.e. not in old list */
        delete from /* Remove old ones */
            public.demo__link
            where
                id
                in
                (
                select
                    old_link.id
                from
                    demo__link old_link
                    left outer join unnest(_links) new_link
                        on
                            new_link.entity_id=old_link.entity_id
                            and
                            new_link.link_type=old_link.link_type
                            and
                            new_link.link_id=old_link.link_id
                where
                    old_link.entity_type=(select numeric from public.demo__definition where category='EntityType' and label='Person')
                    and
                    old_link.entity_id=_id
                    and
                    new_link.entity_id is null /* I.e. not in new list */
                );
    end if;
    return _id;
end;
$$ language plpgsql;

/*
select
    demo_save_person
        (
        '', -- _saved_by varchar(256),
        0, -- _id int,
        array[row(0,0,0),]::demo_link_type[], -- _links demo_link_type[],
        '', -- _email varchar(256),
        '', -- _first_name varchar(256),
        '' -- _last_name varchar(256)
        )
*/

