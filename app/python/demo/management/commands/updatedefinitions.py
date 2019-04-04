from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.management import call_command

# python app\python\manage.py updatedefinitions

class Command(BaseCommand):
    help = \
        """
        This command is to update the definitions table.
        First the existing definition table is backed up (definition_backup), truncated and then restored with the content of the defintions.json fixture
        """

    def handle(self, *args, **options):
        try:
            sql_statement = \
                """
                drop table if exists demo__definition_backup;
                select * into demo__definition_backup from demo__definition;
                truncate table demo__definition;
                """
            with connection.cursor() as c:
                c.execute(sql_statement)
            call_command('loaddata', 'definitions.json')
        except Exception as e:
            raise CommandError(e)

