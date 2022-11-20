import websockets
import asyncio
import numpy as np
import pickle

matrix = np.array([[1,1,1],[2,2,2],[3,3,3]])  #video matrix -- 1
rules = "" #here comes json --2 
status = "" #for status light --3
cam_id = "" #id of the camera --4 
portname = 8001
print("run printhelp to know what to do")

      
    
async def handler (websocket):
    while True:
        rules = await websocket.recv()
        picl = pickle.dumps(matrix)
        await websocket.send(picl)
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