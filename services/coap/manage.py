import asyncio
from project import server
from database import create_tables, create_db
import sys


def run_server():
    asyncio.run(server())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'create_tables':
            create_tables()
        elif cmd == 'create_db':
            create_db()
    run_server()
