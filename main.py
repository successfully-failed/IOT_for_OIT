from detect import detect as PoseDetect
from detector import Detector
import datetime

import cv2

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

def start_detect():
    img_list, mask_lists, img0_list = [], [], []
    diff_x_list, diff_y_list, diff_z_list = [], [], []
    kx_list = []

    standings = 0
    stomachaches = 0

    for dataset in datasets:
        img, mask_list, left_eye_zone, right_eye_zone, diff_x_list, diff_y_list, diff_z_list, kx_list, stomachache, img0 = p_detect.detect2(dataset)

        # Process on persons:
        for person in range(len(kx_list)):
            if detector.is_standing(kx_list[person], diff_y_list[person]): 
                standings += 1
            else:
                standings = 0

            if not detector.eye_detector(left_eye_zone[person], right_eye_zone[person]) and stomachache:
                stomachaches+=1
            else:
                stomachaches = 0

        if standings >= 3:
            print('Standing')
            standings = 0
        if stomachaches >= 3:
            print('Stomachache')
            stomachaches = 0

        img_list.append(img)
        mask_lists.append(mask_list)
        img0_list.append(img0)


    cv2.imshow('image',img_list[0])
    cv2.waitKey(1)
    start_detect()

start_detect()
 