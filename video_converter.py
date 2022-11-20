import numpy as np
import cv2 as cv
import base64 as b64


video = cv.VideoCapture('test_vid.mp4')

def encode (video):
    while True:
        ret, frame = video.read()
        if(ret == False):
            break
        encoded = b64.b64encode(frame)
        return encoded
