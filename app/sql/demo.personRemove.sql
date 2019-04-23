create or replace function
demo_remove_person
    (
    _saved_by varchar(256),
    _id int
    )
returns int as
$$
begin
    if not _id=0 then /* If it is valid */
        insert into /* Audit current item */
            public.demo_person_audit
                (
                saved_on,
                saved_by,
                person_id,
                email,
                first_name,
                last_name,
                type
                )
            select
                saved_on,
                saved_by,
                id,
                email,
                first_name,
                last_name,
                type
            from
                public.demo_person
            where
                id=_id;
        insert into /* Audit deletion */
            public.demo_person_audit
                (
                saved_on,
                saved_by,
                person_id,
                email,
                first_name,
                last_name,
                type
                )
            select
                now(),
                _saved_by,
                id,
                email,
                first_name,
                last_name,
                type
            from
                public.demo_person
            where
                id=_id;
        delete from
            public.demo__link
                where
                    entity_id=_id
                    and
                    entity_type=(select numeric from public.demo__definition where category='EntityType' and label='Person');
        delete from
            public.demo_person
                where
                    id=_id;
    end if;
    return _id;
end;
$$ language plpgsql;

