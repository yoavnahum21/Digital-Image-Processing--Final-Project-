import cv2

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

    
if __name__ == '__main__':
    def image_show(frame):
        edges = cv2.Canny(frame, 100, 200)
        cv2.imshow("Digital Image Processing", edges)
        cv2.waitKey(100)
