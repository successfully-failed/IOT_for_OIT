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
                print("Eyes are closed")
            else:
                print("Eyes are open")
        except:pass
