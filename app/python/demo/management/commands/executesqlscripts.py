from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Drops all existing Postgres functions then executes all sql files in app/sql folder. The sql scripts need to be re-runable.'

    def execute_sql_file(self, file_path):
        sql_statement = open(file_path).read()
        with connection.cursor() as c:
            c.execute(sql_statement)

    def handle(self, *args, **options):
        try:
            sql_statement = \
                """
                do
                    $do$
                    declare
                    function_definition_cursor cursor for
                        select
                            routines.routine_name
                            ||
                            (
                                select
                                    '(' || replace(trim(coalesce(array_agg( parameter )::text,''),'{}'),'"','') || ')' as parameter_list
                                from
                                    (
                                    select
                                        parameters.parameter_name || ' ' || replace(parameters.data_type,'ARRAY','plus_link_type[]') as parameter
                                    from
                                        information_schema.parameters
                                    where
                                        parameters.specific_name=routines.specific_name
                                    order by
                                        parameters.ordinal_position
                                    ) parameters
                            ) as function_definition
                        from
                            information_schema.routines
                        where
                            routines.specific_name like 'plus_%'
                        order by
                            routines.routine_name;
                    function_definition_record record;
                    drop_command text;
                    begin
                        open function_definition_cursor;
                        loop
                            fetch next from function_definition_cursor into function_definition_record;
                            exit when not found;
                            drop_command := 'drop function ' || function_definition_record.function_definition || ';';
                            execute drop_command;
                        end loop;
                        close function_definition_cursor; 
                    end
                    $do$
                """
            with connection.cursor() as c:
                c.execute(sql_statement)
            sql_dir = os.path.join(os.path.abspath(os.path.join(settings.BASE_DIR, os.pardir)), 'sql')
            if not os.path.isdir(sql_dir):
                raise CommandError('The sql folder could not be found. Script should be in: %s' % sql_dir)
            sql_files = [os.path.join(sql_dir, f) for f in os.listdir(sql_dir) if os.path.isfile(os.path.join(sql_dir, f)) and (f.find('.sql') != -1)]
            for sql_file in sorted(sql_files):
                self.execute_sql_file(sql_file)
        except Exception as e:
            raise CommandError('Error: ' % str(e))

