import cv2
from matplotlib import pyplot as plt
import numpy as np

''' This file contains the player class with the following attributes and methods:
1. name - self explanatory
2. get_curr_pos - reads camera frame and determines hand position.'''


class Player:
    def __init__(self, name):
        self.name = name
        self.zero_pos = None
        self.max_pos = None
        self.min_pos = None

    def get_curr_pos(self):
        # TODO: write method to read frame from camera and detect hand position
        pass


def mask_skin_color(img):
    rgba_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hsv_img = cv2.normalize(cv2.cvtColor(img, cv2.COLOR_RGB2HSV), None, 0, 1, norm_type=cv2.NORM_MINMAX,
                            dtype=cv2.CV_32F)
    ys = 480
    xs = 640
    for y in range(ys):
        for x in range(xs):
            h = hsv_img[y,x,0]
            s = hsv_img[y,x,1]
            r = rgba_img[y,x,0]
            g = rgba_img[y,x,1]
            b = rgba_img[y,x,2]
            a = rgba_img[y,x,3]
            if h <= 0.50 and 0.23 <= s <= 0.68 and r > 95 and g > 40 and b > 20 and a > 15 and r > g > b and np.abs(r - g) > 15:
                pass
            else:
                img[y, x, :] = 0
    return img




if __name__ == '__main__':
    hand_cam = cv2.VideoCapture(1)
    counter = 0
    # while True:
    #     _, frame = hand_cam.read()
    #     frame = cv2.rectangle(frame, (60, 160), (220, 320), (0, 255, 0), 3)
    #     frame = cv2.rectangle(frame, (580, 160), (420, 320), (0, 255, 0), 3)
    #     frame = cv2.flip(frame, 1)
    #     cv2.imshow("frame", frame)
    #     cv2.waitKey(1)
    #     counter += 1
    #     if counter == 100:
    #         break
    # right_ref = frame[160:320, 420:580, :]
    # left_ref = frame[160:320, 60:220, :]
    # cv2.imshow("left hand", left_ref[:,:,0])
    # cv2.imshow("right_ref", right_ref[:,:,0])
    # cv2.waitKey(0)
    #
    # _, left_b = cv2.threshold(left_ref[:, :, 0], 20, 255,  cv2.THRESH_BINARY)
    # _, left_g = cv2.threshold(left_ref[:, :, 1], 40, 255, cv2.THRESH_BINARY)
    # _, left_r = cv2.threshold(left_ref[:, :, 2], 95, 255, cv2.THRESH_BINARY)
    # rnb = cv2.bitwise_and(left_b, left_r)
    # rnbng = cv2.bitwise_and(rnb, left_g)
    # cv2.imshow("mask", rnbng)
    # cv2.waitKey(0)
    # # convert to grayscale and pyrdown
    # right_ref = cv2.cvtColor(right_ref, cv2.COLOR_BGR2GRAY)
    # left_ref = cv2.cvtColor(left_ref, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("left hand gray", left_ref)
    # cv2.imshow("right hand gray", right_ref)
    # cv2.waitKey(0)
    # right_2 = cv2.pyrDown(right_ref)
    # cv2.imshow("right_2", right_2)
    # cv2.waitKey(0)
    # right_4 = cv2.pyrDown(right_2)
    # cv2.imshow("right_4", right_4)
    # cv2.waitKey(0)
    # left_2 = cv2.pyrDown(left_ref)
    # cv2.imshow("left_2", left_2)
    # cv2.waitKey(0)
    # left_4 = cv2.pyrDown(left_2)
    # cv2.imshow("left_4", left_4)
    # cv2.waitKey(0)

    sift = cv2.SIFT_create(100, 3, contrastThreshold=0.04, edgeThreshold=10, sigma=2)
    # left_keys, left_des = sift.detectAndCompute(left_ref, None)
    # left_hand_keys = cv2.drawKeypoints(left_ref, left_keys, None)
    # cv2.imshow("left_keys", left_hand_keys)
    # cv2.waitKey(0)
    # right_keys, right_des = sift.detectAndCompute(right_ref, None)
    # right_hand_keys = cv2.drawKeypoints(right_ref, right_keys, None)
    # cv2.imshow("right_keys", right_hand_keys)
    # cv2.waitKey(0)
    # print(left_des[0])


    #frame = cv2.imread("camera_test/test_frame.png")
    # _, frame = hand_cam.read()
    # cv2.imwrite("camera_test/test_frame.png", frame)
    cv2.imshow("b", frame[:,:,0])
    cv2.waitKey(0)
    cv2.imshow("g", frame[:,:,1])
    cv2.waitKey(0)
    cv2.imshow("r", frame[:,:,2])
    cv2.waitKey(0)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    cv2.imshow("l", frame[:, :, 0])
    cv2.waitKey(0)
    cv2.imshow("a", frame[:, :, 1])
    cv2.waitKey(0)
    cv2.imshow("b", frame[:, :, 2])
    cv2.waitKey(0)
    cv2.imshow("a1", frame[:, :, 1])
    cv2.waitKey(0)