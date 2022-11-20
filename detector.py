import tensorflow as tf 
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import datetime, json

class Detector:
    def __init__(self) -> None:
        self.model = load_model('models/binary_closed_eye_model.h5')
        self.lower_range = np.array([0,0,168])
        self.upper_range = np.array([172,111,255])
        self.log_file = "log/log.json"
        self.no_somebody = 0
        self.two_persons = 0
        self.no_drip_nr = 0
        
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

    def drip_bag_detector(self, drip_zone, cam_id):
        hsv = cv2.cvtColor(drip_zone, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        suma = 0
        
        for nr, i in enumerate(mask):
            for j in mask[nr]:
                if j == 255:
                    suma += 1
        if suma > 35:
            print("Drip detected")
            self.no_drip_nr = 0
        else:
            self.no_drip_nr += 1
            if self.no_drip_nr >= 10:
                self.no_drip_nr = 0
                print("NO DRIP!")
                self.logg(cam_id, "No drip detected!")

    def is_standing(self, scale, diff_y) -> bool:
        # [pl] diff_z nie działa, opncv błędnie go wykrywa, więc go tu nie użyłem
        if diff_y > 2*scale:
            return True
        else: return False

    def logg(self, camera_id, action):
        with open(self.log_file,'r+') as file:
            file_data = json.load(file)

            try:
                id = file_data["logs"][len(file_data["logs"])-1]["_id"]+1
            except:
                id = 0

            file_data["logs"].append({
                "_id": id,
                "timestamp": int(datetime.datetime.now().timestamp()*1000),
                "camera_id": camera_id,
                "action": action
            })
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    def image_analyse(self, kx_list, diff_y_list, stomachache, interval, standings, stomachaches, wait_to_standings, wait_to_stomachaches, cam_id):
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
            self.no_somebody = 0
            if self.two_persons == 0:
                print('Nurse or doctor is here!')
                self.logg(cam_id, "Nurse or doctor service")
                self.two_persons += 1
            else:
                self.two_persons += 1
                if self.two_persons >= 3:
                    self.two_persons = 0
        else:
            self.no_somebody += 1
            self.two_persons = 1
            if self.no_somebody >= 3:
                print('No one here! PROGRAM PASSIVE WORKING')
                self.logg(cam_id, "No one in room.")
                self.no_somebody = 0
        
        if standings >= 3:
            print('Standing proofed')
            self.logg(cam_id, "Patient standing")
            standings = 0
            wait_to_standings = datetime.datetime.now().timestamp() + interval
        if stomachaches >= 3:
            print('Stomachache proofed')
            self.logg(cam_id, "Patient have stomachache")
            stomachaches = 0
            wait_to_stomachaches = datetime.datetime.now().timestamp() + interval

        return [standings, stomachaches, wait_to_standings, wait_to_stomachaches]