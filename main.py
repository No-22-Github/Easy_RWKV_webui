import asyncio
from pywebio import start_server
from chat_room.chat_room import main

if __name__ == '__main__':
    asyncio.run(start_server(main, debug=True, port=8080))
