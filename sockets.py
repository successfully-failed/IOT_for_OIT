import websockets
import asyncio
import video_converter as vide



vid = "" 
rules = "" #here comes json --2 
status = "" #for status light --3
cam_id = "" #id of the camera --4 
portname = 8001
print("run printhelp to know what to do")

      
    
async def handler (websocket):
    while True:
        rules = await websocket.recv()
        await websocket.send(vid)
        await websocket.send(rules)
        await websocket.send(status)
        await websocket.send(cam_id)
        #tester = await websocket.recv()
        #print(tester)


async def main (): 
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

#def printhelp(:
 #   print("After creating an object run main method with assync.runner.run()")

asyncio.run(main())
