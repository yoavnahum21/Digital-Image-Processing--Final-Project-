""" This file is about the race car class. Break down of class attributes and
methods:
1.

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


class RaceCar:
    def __init__(self):
        self.location = None
        self.velocity = None

    def get_car_pos(self, frame):
        pass


if __name__ == '__main__':
    filepath = 'camera_test/44.023.png'
    frame = cv2.imread(filepath)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.equalizeHist(grayFrame)

    # hist = cv2.calcHist([grayFrame], [0], None, [256], (0, 256))
    # plt.plot(hist, color='b')
    # plt.xlim([0, 256])
    # plt.show()
    cv2.imshow("frame", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



