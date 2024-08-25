from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = "Drops all tables and applies migrations"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("Database reset successfully"))