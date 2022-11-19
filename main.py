from detect import detect as PoseDetect
from detector import Detector
import datetime

import cv2

# Settings
interval = 5

cam_view = []
cam_list = []
cam_nr = 0
first_time = True
weights_pose = "PoseModule/yolov7/yolov7-w6-pose.pt"
view_img = True
imgsz = 640
half_precision = True
kpt_label = True
device = ''  # GPU, if cpu = 'cpu'
conf_thres = .75
iou_thres = .45
classes = False
agnostic_nms = False
line_thickness = 8
empty = []
p_detect = PoseDetect(
    weights_pose, 
    view_img, 
    imgsz, 
    half_precision, 
    kpt_label, 
    device, 
    conf_thres, 
    iou_thres, 
    classes, 
    agnostic_nms, 
    line_thickness
)
datasets = p_detect.setup()
detector = Detector()

def start_detect(standings, stomachaches, wait_to_standings, wait_to_stomachaches):
    img_list, mask_lists, img0_list = [], [], []
    diff_x_list, diff_y_list, diff_z_list = [], [], []
    kx_list = []

    for dataset in datasets:
        img, mask_list, left_eye_zone, right_eye_zone, diff_x_list, diff_y_list, diff_z_list, kx_list, stomachache, img0 = p_detect.detect2(dataset)
        # Process on persons:
        if len(kx_list) == 1:
            if datetime.datetime.now().timestamp() >= wait_to_standings:
                if detector.is_standing(kx_list[0], diff_y_list[0]):
                    print('Standing!')
                    standings += 1
                else:
                    standings = 0

            if datetime.datetime.now().timestamp() > wait_to_standings:
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

        img_list.append(img)
        mask_lists.append(mask_list)
        img0_list.append(img0)


    cv2.imshow('image',img_list[0])
    cv2.waitKey(1)
    start_detect(standings, stomachaches, wait_to_standings, wait_to_stomachaches)

start_detect(0, 0, 0, 0)
 