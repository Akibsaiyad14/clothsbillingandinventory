"""
Management command to create PostgreSQL database
"""
from django.core.management.base import BaseCommand
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Create PostgreSQL database if it does not exist'

    def handle(self, *args, **options):
        db_name = os.getenv('DB_NAME', 'clothshop_db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')

        try:
            # Connect to PostgreSQL server
            conn = psycopg2.connect(
                dbname='clothBilling',
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Check if database exists
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )
            exists = cursor.fetchone()

            if exists:
                self.stdout.write(
                    self.style.WARNING(f'Database "{db_name}" already exists')
                )
            else:
                # Create database
                cursor.execute(f'CREATE DATABASE {db_name}')
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created database "{db_name}"')
                )

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('\nMake sure PostgreSQL is running and credentials in .env are correct')
            )
