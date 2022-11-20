import asyncio
from sockets import Socket_manager as Soc
import websockets

soc = Soc()
asyncio.run(soc.main())
