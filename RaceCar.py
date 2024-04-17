from big_code_version import FrameProcessor
import cv2
import math
import numpy as np


class RaceCar:
    def __init__(self, camera):
        self.location = np.array([0,0])
        self.velocity = None
        self.orientation = None
        self.car_cam = camera
        self.car_pick = None
        self.car_img = None

    # set self.car_img to be an image taken from camera
    def take_img(self):
        _, frame = self.car_cam.read()
        self.car_img = frame
        #self.car_cam.release()

    # sets self.location to be car coordinates in (y,x)
    def get_car_pos(self, persp_mat, first_frame):
        if first_frame:
            (self.prev_x, self.prev_y, constant_radius, first_frame, self.lower_white,
             self.upper_white) = initialize_tracking()
        else:
            self.new_x, self.new_y, self.found, self.mask, self.contours, self.lower_white, self.upper_white = (
                process_frame(self.car_img, self.lower_white, self.upper_white, first_frame, self.prev_x, self.prev_y))
            self.location = np.matmul(persp_mat, np.array([self.new_x, self.new_y]))

    # sets self.velocity to be car velocity magnitude
    def get_velocity_n_orientation(self):
        frame_rate = self.car_cam.get(cv2.CAP_PROP_FPS)
        scale_x, scale_y = (2.5 / self.car_cam.get(cv2.CAP_PROP_FRAME_WIDTH),
                            2 / self.car_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.found and self.prev_x is not None and self.prev_y is not None:
            self.velocity, self.orientation = calculate_speed_and_orientation(self.prev_x, self.prev_y, self.new_x,
                                                                              self.new_y, scale_x, scale_y, frame_rate)

    # returns a rotated binary image of car surroundings
    def get_surrounding(self, img):
        window = get_window(img, self.location, 50)
        window = cv2.resize(window, (700, 700), interpolation=cv2.INTER_AREA)
        # ang = 90 + math.degrees(math.atan2(self.orientation[1], self.orientation[0]))
        rot_mat = cv2.getRotationMatrix2D((350, 350), self.orientation, 1.0)
        return cv2.warpAffine(window, rot_mat, (700, 700), cv2.INTER_NEAREST, cv2.BORDER_CONSTANT)

    # sets self.orientation to the direction car is facing
    # def get_orientation(self, persp_mat):
    #     pass
        # TODO: use get_window to get car image and detect car orientation. then use persp_mat to get
        #  orientation in stretched image. return orientation as a 2D vector - deprecated


def get_window(track_img, car_pos, size):
    x = car_pos[0]
    y = car_pos[1]
    window = track_img[y-size:y+size, x-size: x+size]
    return window


def initialize_tracking():
    return None, None, 25, True, np.array([0, 0, 168], dtype=np.uint8), np.array([172, 111, 255], dtype=np.uint8)


def update_search_area(frame_shape, prev_x, prev_y, margin_scale=0.1):
    margin_x = int(frame_shape[1] * margin_scale)
    margin_y = int(frame_shape[0] * margin_scale)
    x_min = max(0, prev_x - margin_x)
    x_max = min(frame_shape[1], prev_x + margin_x)
    y_min = max(0, prev_y - margin_y)
    y_max = min(frame_shape[0], prev_y + margin_y)
    return x_min, x_max, y_min, y_max


def process_frame(frame, lower_white, upper_white, first_frame, prev_x, prev_y):
    if first_frame:
        x_min, y_min, x_max, y_max = 0, 0, frame.shape[1], frame.shape[0]
    else:
        x_min, x_max, y_min, y_max = update_search_area(frame.shape, prev_x, prev_y)

    cropped_frame = frame[y_min:y_max, x_min:x_max]
    hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    found, new_x, new_y = False, prev_x, prev_y
    if contours:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        new_x, new_y = int(x) + x_min, int(y) + y_min
        found = True

        # Convert x, y, and radius to integers for precise ROI calculation
        x, y, radius = int(x), int(y), int(radius)

        # Calculate bounds for ROI
        roi_x_min = max(0, x - int(radius * 0.7))
        roi_x_max = min(mask.shape[1], x + int(radius * 0.7))
        roi_y_min = max(0, y - int(radius * 0.7))
        roi_y_max = min(mask.shape[0], y + int(radius * 0.7))

        # Extract ROI from the mask and HSV image
        mask_roi = mask[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
        hsv_roi = hsv[roi_y_min:roi_y_max, roi_x_min:roi_x_max]

        # Calculate new HSV range based on the mean color within the inner part of the detected object
        mean_val = cv2.mean(hsv_roi, mask=mask_roi)
        lower_white = np.array([max(mean_val[0] - 20, 0), max(mean_val[1] - 60, 0), max(mean_val[2] - 50, 0)],
                               dtype=np.uint8)
        upper_white = np.array([min(mean_val[0] + 20, 180), min(mean_val[1] + 50, 255), min(mean_val[2] + 50, 255)],
                               dtype=np.uint8)

    return new_x, new_y, found, mask, contours, lower_white, upper_white


def calculate_speed_and_orientation(prev_x, prev_y, new_x, new_y, scale_x, scale_y, frame_rate):
    dx = (new_x - prev_x) * scale_x
    dy = (new_y - prev_y) * scale_y
    speed = np.sqrt(dx ** 2 + dy ** 2) * frame_rate
    orientation = np.arctan2(dy, dx)
    return speed, orientation



if __name__ == '__main__':
    pass

