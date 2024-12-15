from django.core.management.base import BaseCommand
from time import sleep
from django.db import connections
from psycopg2 import OperationalError


class Command(BaseCommand):
    help = "Wait for the database to be ready"

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database...\n")
        db_up = False
        while not db_up:
            try:
                # Перевірка підключення до бази даних
                connection = connections["default"]
                connection.cursor()
                db_up = True
                self.stdout.write(self.style.SUCCESS("Database is ready!"))
            except OperationalError:
                self.stdout.write("Database not ready, waiting 1 second...\n")
                sleep(1)
