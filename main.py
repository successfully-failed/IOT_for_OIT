from detect import detect as PoseDetect
from detector import Detector

import cv2

# Settings
interval = 30

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
line_thickness = 2
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
datasets, cams_id = p_detect.setup()
detector = Detector()

def start_detect(standings, stomachaches, wait_to_standings, wait_to_stomachaches):
    img_list, mask_lists, img0_list = [], [], []
    diff_x_list, diff_y_list, diff_z_list = [], [], []
    kx_list = []
    danger_list = []

    for i in range(len(datasets)):
        try:
            img, mask_list, left_eye_zone, right_eye_zone, diff_x_list, diff_y_list, diff_z_list, kx_list, stomachache, drip_zone_list, img0 = p_detect.detect2(datasets[i])
            
            temp_data = detector.image_analyse(kx_list, diff_y_list, stomachache, interval, standings, stomachaches, wait_to_standings, wait_to_stomachaches, cam_id=cams_id[i])
            standings = temp_data[0]
            stomachaches = temp_data[1]
            wait_to_standings = temp_data[2] 
            wait_to_stomachaches = temp_data[3]
            danger = temp_data[4]


            if len(drip_zone_list):
                danger2 = detector.drip_bag_detector(drip_zone_list[0], cam_id=cams_id[i])  

            if danger2:
                danger_list.append(2)
            elif danger:
                danger_list.append(1)
            else: danger_list.append(0)   
                
            img_list.append(img)
        except: print("Video has ended")

    detector.data_setter(img_list, cams_id, danger_list)
        
    cv2.imshow('image',img_list[0])
    cv2.waitKey(1)
    start_detect(standings, stomachaches, wait_to_standings, wait_to_stomachaches)

start_detect(0,0,0,0)
 