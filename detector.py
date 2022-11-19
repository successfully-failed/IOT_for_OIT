import tensorflow as tf 
import numpy as np
from tensorflow.keras.models import load_model

class Detector:
    def __init__(self) -> None:
        self.model = load_model('models/binary_closed_eye_model.h5')
        
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
    
    @staticmethod
    def is_standing(scale, diff_y) -> bool:
        # [pl] diff_z nie działa, opncv błędnie go wykrywa, więc go tu nie użyłem
        if diff_y > 2*scale:
            return True
        else: return False
