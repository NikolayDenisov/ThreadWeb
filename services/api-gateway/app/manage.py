import psycopg2
from table_init import commands
import os


def create_db():
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://"))
        cursor = conn.cursor()
        for command in commands:
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
