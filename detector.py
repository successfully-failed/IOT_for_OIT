import tensorflow as tf 
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import datetime

class Detector:
    def __init__(self) -> None:
        self.model = load_model('models/binary_closed_eye_model.h5')
        self.lower_range = np.array([0,0,168])
        self.upper_range = np.array([172,111,255])
        
    def eye_detector(self, left_eye, right_eye):
        try:
            resize_l = tf.image.resize(left_eye, (256, 256))
            resize_r = tf.image.resize(right_eye, (256, 256))

            pred_l = self.model.predict(np.expand_dims(resize_l / 255, 0))
            pred_r = self.model.predict(np.expand_dims(resize_r / 255, 0))
            if (pred_l < .1) and (pred_r < .1):
                return False # False = eyes closed
            else:
                return True # True = eyes open
        except:pass

    def drip_bag_detector(self, drip_zone):
        hsv = cv2.cvtColor(drip_zone, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        suma = 0
        
        for nr, i in enumerate(mask):
            for j in mask[nr]:
                if j == 255:
                    suma += 1
        if suma > 35:
            print("Drip detected")
            return True 
        else:
            print("NO DRIP!")
            return False

    def is_standing(self, scale, diff_y) -> bool:
        # [pl] diff_z nie działa, opncv błędnie go wykrywa, więc go tu nie użyłem
        if diff_y > 2*scale:
            return True
        else: return False

    def image_analyse(self, kx_list, diff_y_list, stomachache, interval, standings, stomachaches, wait_to_standings, wait_to_stomachaches):
        if len(kx_list) == 1:
            if datetime.datetime.now().timestamp() >= wait_to_standings:
                if self.is_standing(kx_list[0], diff_y_list[0]):
                    print('Standing!')
                    standings += 1
                else:
                    standings = 0

            if datetime.datetime.now().timestamp() > wait_to_stomachaches:
                if stomachache:
                    stomachaches+=1
                    print('Stomachache')
                else:
                    stomachaches = 0
        elif len(kx_list) > 1:
            print('Nurse or doctor is here!')
        else:
            print('No one here! PROGRAM PASSIVE WORKING')

        
        if standings >= 3:
            print('Standing proofed')
            standings = 0
            wait_to_standings = datetime.datetime.now().timestamp() + interval
        if stomachaches >= 3:
            print('Stomachache proofed')
            stomachaches = 0
            wait_to_stomachaches = datetime.datetime.now().timestamp() + interval

        return [standings, stomachaches, wait_to_standings, wait_to_stomachaches]