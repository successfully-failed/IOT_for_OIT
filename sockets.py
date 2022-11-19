import websockets
import asyncio
import numpy as np
import pickle

class Socket_manager ():
    def __init__ (self):
        self.matrix = np.array([[1,1,1],[2,2,2],[3,3,3]])  #video matrix -- 1
        self.rules = "" #here comes json --2 
        self.status = "" #for status light --3
        self.cam_id = "" #id of the camera --4 
        self.__portname = 8001
        print("run printhelp to know what to do")

    def __del__ (self):
        del self.matrix
        del self.rules
        del self.status
        del self.cam_id
        del self.__portname
    
#choice - choose the fied of the function, arg - arguments for getter and setter
    def setter (self,choice, arg):
        if(choice == 1):
            self.matrix = arg
        elif(choice == 2):
            self.rules = arg
        elif(choice == 3):
            self.status = arg
        elif(choice == 4):
            self.status = arg
    
    def getter (self,choice, arg):
        if(choice == 1):
            return self.matrix
        elif(choice == 2):
            return self.rules
        elif(choice == 3):
            return self.status
        elif(choice == 4):
            return self.cam_id


        
    async def handler (self, websocket):
        while True:
            self.rules = await websocket.recv()
            picl = pickle.dumps(self.matrix)
            await websocket.send(picl)
            await websocket.send(self.rules)
            await websocket.send(self.status)
            await websocket.send(self.cam_id)
            tester = await websocket.recv()
            print(tester)


    async def main (self):
        handler = self.handler
        async with websockets.serve(handler, "", 8001):
            await asyncio.Future()
    
    def printhelp(self):
        print("After creating an object run main method with assync.runner.run()")
   

