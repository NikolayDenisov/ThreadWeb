import psycopg2
from table_init import commands
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db():
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://"))
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'example'")
        exists = cursor.fetchone()
        if not exists:
            run_commands = commands[:]
        else:
            run_commands = commands[5:]
        for command in run_commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_db()
