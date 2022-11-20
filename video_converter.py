import numpy as np
import cv2 as cv
import base64 as b64

class Encoder ():
    def __init__ (self):
        self.video = cv.VideoCapture('test_vid.mp4')
        self.encode()

    def encode (self):
        while True:
            ret, frame = self.video.read()
            if(ret == False):
                break
            encoded = b64.b64encode(frame)
            return encoded
