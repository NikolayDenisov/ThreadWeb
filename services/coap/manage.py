import asyncio
from project import server


def run_server():
    asyncio.run(server())


if __name__ == "__main__":
    run_server()
