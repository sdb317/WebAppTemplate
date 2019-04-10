import os

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
            app = os.path.basename(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
            sql_statement = \
                """
                drop table if exists {0}__definition_backup;
                select * into {0}__definition_backup from {0}__definition;
                truncate table {0}__definition;
                """.format(app)
            with connection.cursor() as c:
                c.execute(sql_statement)
            call_command('loaddata', 'definitions.json')
        except Exception as e:
            raise CommandError(e)

