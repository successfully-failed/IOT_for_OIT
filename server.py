import asyncio
from sockets import Socket_manager
import websockets

manager = Socket_manager()
manager.start()
print(manager.rules)
