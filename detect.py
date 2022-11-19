import torch.backends.cudnn as cudnn
import cv2
import torch
import os

from PoseModule.yolov7.models.experimental import attempt_load
from PoseModule.yolov7.utils.datasets import LoadStreams, LoadImages
from PoseModule.yolov7.utils.plots import colors, plot_one_box
from PoseModule.yolov7.utils.torch_utils import select_device, load_classifier
from PoseModule.yolov7.utils.general import check_img_size, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, set_logging


class detect:

    def __init__(self, weights, view_img, imgsz, half_precision, kpt_label, device, conf_thres, iou_thres, classes, agnostic_nms, line_thickness) -> None:

        self.imgsz = imgsz
        self.kpts = None
        self.view_img = view_img
        self.kpt_label = kpt_label
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.agnostic_nms = agnostic_nms
        self.line_thickness = line_thickness
        self.classes = classes
        self.weights = weights
        self.half_precision = half_precision
        self.device = device

    def setup(self):
        with torch.no_grad():
            cameras = []
            cam_list = self.check_available_cameras()
            # cam_list = []
            for filename in os.listdir("videos/"):
                if filename.endswith(".mp4"):
                    cam_list.append(f"videos/{filename}")

            set_logging()
            self.device = select_device(self.device)
            self.half = self.device.type != 'cpu' and self.half_precision

            self.model = attempt_load(self.weights, map_location=self.device)
            self.stride = int(self.model.stride.max())

            if isinstance(self.imgsz, (list, tuple)):
                assert len(self.imgsz) == 2
                "height and width of image has to be specified"
                self.imgsz[0] = check_img_size(self.imgsz[0], s=self.stride)
                self.imgsz[1] = check_img_size(self.imgsz[1], s=self.stride)
            else:
                self.imgsz = check_img_size(self.imgsz, s=self.stride)
            self.names = self.model.module.names if hasattr(
                self.model, 'module') else self.model.names

            if self.half:
                self.model.half()

            self.classify = False
            if self.classify:
                self.modelc = load_classifier(name='resnet101', n=2)
                self.modelc.load_state_dict(torch.load(
                    'weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

            if self.device.type != 'cpu':
                self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(
                    self.device).type_as(next(self.model.parameters())))

            for source in cam_list:
                source = str(source)
                self.webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
                    ('rtsp://', 'rtmp://', 'http://', 'https://'))
                if self.webcam:
                    cudnn.benchmark = True
                    dataset = LoadStreams(
                        source, img_size=self.imgsz, stride=self.stride)
                else:
                    dataset = LoadImages(
                        source, img_size=self.imgsz, stride=self.stride)
                cameras.append(dataset)
            return cameras

    def detect2(self, dataset):
        with torch.no_grad():
            i = 0
            for path, img, im0s, vid_cap in dataset:
                i += 1
                if i % 20 == 0:
                    img = torch.from_numpy(img).to(self.device)
                    img = img.half() if self.half else img.float()
                    img /= 255.0
                    if img.ndimension() == 3:
                        img = img.unsqueeze(0)
                    pred = []
                    pred = self.model(img, augment=False)[0]
                    pred = non_max_suppression(pred, self.conf_thres, self.iou_thres,
                                               classes=self.classes, agnostic=self.agnostic_nms, kpt_label=self.kpt_label)

                    if self.classify:
                        pred = apply_classifier(pred, self.modelc, img, im0s)

                    mask_list = []
                    left_eyes = []
                    right_eyes = []
                    diff_x_list = []
                    diff_y_list = []
                    diff_z_list = []
                    kx_list = []


                    for i, det in enumerate(pred):
                        if isinstance(dataset, LoadStreams):
                            im0 = im0s[i].copy()
                            im1 = im0s[i].copy()
                        elif isinstance(dataset, LoadImages):
                            im0 = im0s.copy()
                            im1 = im0s.copy()

                        if len(det):
                            scale_coords(
                                img.shape[2:], det[:, :4], im0.shape, kpt_label=False)
                            scale_coords(
                                img.shape[2:], det[:, 6:], im0.shape, kpt_label=self.kpt_label, step=3)

                            for det_index, (*xyxy, conf, cls) in enumerate(reversed(det[:, :6])):
                            
                                c = int(cls)
                                label = None if False else (
                                    self.names[c] if False else f'{self.names[c]} {conf:.2f}')
                                kpts = det[det_index, 6:]
                                step = 3
                                nr = 0  # 0-nose, 1-left eye, 2-right eye, 3-left ear, 4-right ear, 5-left shouder, 6-right shouder, 11-left hip, 12-right hip

                                # mouth point - for mask
                                x_center, y_nose = kpts[step *
                                                        nr], kpts[step * nr + 1]
                                y_shouder_l, y_shouder_r = kpts[step *
                                                                5 + 1], kpts[step * 6 + 1]
                                y_shouders = (
                                    (y_shouder_l + y_shouder_r) / 2)
                                y_center = abs(
                                    (y_shouders - y_nose) / 2.0) + y_nose
                                #cv2.circle(im0, (int(x_center), int(y_center)), 6, (0,0,255), -1)

                                # mask zone
                                x_start_mask = int(kpts[step * 1])
                                x_end_mask = int(kpts[step * 2])
                                x_length = abs(x_end_mask - x_start_mask)
                                x_length = x_length / 2
                                y_start_mask = int(y_nose)
                                y_end_height = int(y_center)
                                y_length = abs(y_end_height-y_start_mask) /2
                                y_length = y_start_mask + y_length
                                y_start_mask = int(y_length - x_length)
                                y_end_height = int(y_length + x_length)
                                if y_start_mask <= kpts[step * 0 + 1]:
                                    y_start_mask = int(kpts[step * 0 + 1] * 1.05)
                                else:
                                    y_start_mask = int(y_start_mask)

                                mask_zone_img = im1[y_start_mask:y_end_height,
                                                        x_end_mask:x_start_mask]

                            
                                mask_list.append(mask_zone_img)
                                cv2.rectangle(im0, (x_start_mask, y_start_mask), (x_end_mask, y_end_height), color=(
                                    0, 255, 255), thickness=2)

                                #eyes zone
                                distance_to_nose_x = abs(kpts[step * 0] - kpts[step * 1]) * .8
                                distance_to_nose_y = abs(kpts[step * 0 + 1] - kpts[step * 1 + 1])  * .35

                                left_eye_start_x =  int(kpts[step * 1] - distance_to_nose_x)
                                left_eye_end_x =  int(kpts[step * 1] + distance_to_nose_x)
                                left_eye_start_y =  int(kpts[step * 1 + 1] - distance_to_nose_y)
                                left_eye_end_y =  int(kpts[step * 1 + 1] + distance_to_nose_y)
                                left_eye_zone = im1[left_eye_start_y: left_eye_end_y,
                                                    left_eye_start_x:left_eye_end_x]
                                left_eyes.append(left_eye_zone)
                                
                                cv2.rectangle(im0, (left_eye_start_x, left_eye_start_y), (left_eye_end_x, left_eye_end_y), color=(
                                    0, 255, 255), thickness=2)

                                right_eye_start_x =  int(kpts[step * 2] - distance_to_nose_x)
                                right_eye_end_x =  int(kpts[step * 2] + distance_to_nose_x)
                                right_eye_start_y =  int(kpts[step * 2 + 1] - distance_to_nose_y)
                                right_eye_end_y =  int(kpts[step * 2 + 1] + distance_to_nose_y)
                                right_eye_zone = im1[right_eye_start_y: right_eye_end_y,
                                                    right_eye_start_x:right_eye_end_x]
                                right_eyes.append(right_eye_zone)
                                
                                cv2.rectangle(im0, (right_eye_start_x, right_eye_start_y), (right_eye_end_x, right_eye_end_y), color=(
                                    0, 255, 255), thickness=2)

                                left_shouder_x, left_shouder_y = kpts[step * 5], kpts[step * 5 + 1]
                                right_shouder_x, right_shouder_y = kpts[step * 6], kpts[step * 6 + 1]
                                right_hip_x, right_hip_y = kpts[step * 12], kpts[step * 12+ 1]

                                left_hand_x, left_hand_y = kpts[step * 9], kpts[step * 9 + 1]
                                right_hand_x, right_hand_y = kpts[step * 10], kpts[step * 10 + 1]

                                h_x, h_y = False, False
                                if (left_shouder_x > left_hand_x > right_hip_x) and \
                                    (left_shouder_x > right_hand_x > right_hip_x):
                                    h_x = True

                                if (left_shouder_y < left_hand_y < right_hip_y) and \
                                    (left_shouder_y < right_hand_y < right_hip_y):
                                    h_y = True

                                if h_x and h_y:
                                    print("Stomachache")
                                else: print("No Stomachache")


                                head_x, head_y, head_z = int(
                                    kpts[step * 1]), int(kpts[step * 1 + 1]), kpts[step * 1 + 2]

                                hip_x, hip_y, hip_z = int(
                                    kpts[step * 11]), int(kpts[step * 11 + 1]), kpts[step * 11 + 2]


                                shouder_l_x, shouder_l_y, shouder_l_z = int(
                                    kpts[step * 5]), int(kpts[step * 5 + 1]), kpts[step * 5 + 2]
                                shouder_r_x, shouder_r_y, shouder_r_z = int(
                                    kpts[step * 6]), int(kpts[step * 6 + 1]), kpts[step * 6 + 2]    

                                kx = abs(shouder_l_x - shouder_r_x)
                                
                                diff_x = abs(head_x-hip_x)
                                diff_y = hip_y - head_y
                                diff_z = abs(head_z-hip_z)

                                diff_x_list.append(diff_x)
                                diff_y_list.append(diff_y)
                                diff_z_list.append(diff_z)
                                kx_list.append(kx)

                                # Entire body:
                                plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=self.line_thickness, kpt_label=self.kpt_label, kpts=kpts, steps=3, orig_shape=im0.shape[:2])

                        return im0, mask_list, left_eyes, right_eyes, diff_x_list, diff_y_list, diff_z_list, kx_list, im0s

    @staticmethod
    def check_available_cameras():
        cam_list = []
        for i in range(0, 10):
            cap = cv2.VideoCapture(i)
            if cap is None or not cap.isOpened():
                pass
            else:
                cam_list.append(i)
        return cam_list
