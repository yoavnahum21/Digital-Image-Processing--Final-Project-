""" This file is about the race car class. Break down of class attributes and
methods:
1.

"""

import cv2
import math


class RaceCar:
    def __init__(self, camera):
        self.location = None
        self.velocity = None
        self.orientation = None
        self.car_cam = camera
        self.car_pick = None
        self.car_img = None

    # set self.car_img to be an image taken from camera
    def take_img(self):
        self.car_img = self.car_cam.read()
        self.car_cam.release()

    # sets self.location to be car coordinates in (y,x)
    def get_car_pos(self, persp_mat):
        # TODO: take self.car_img, find car coordinates in that img in (x,y) and then use persp_mat to find
        #  coordinates in stretched image. then set self.location to said coordinates
        pass

    # sets self.velocity to be car velocity magnitude
    def get_velocity(self):
        pass
        # TODO: get car velocity magnitude

    # returns a rotated binary image of car surroundings
    def get_surrounding(self, img):
        window = get_window(img, self.location, 50)
        window = cv2.resize(window, (700, 700), interpolation=cv2.INTER_AREA)
        ang = 90 + math.degrees(math.atan2(self.orientation[1], self.orientation[0]))
        rot_mat = cv2.getRotationMatrix2D((350, 350), ang, 1.0)
        return cv2.warpAffine(window, rot_mat, (700, 700), cv2.INTER_NEAREST, cv2.BORDER_CONSTANT)

    # sets self.orientation to the direction car is facing
    def get_orientation(self, persp_mat):
        pass
        # TODO: use get_window to get car image and detect car orientation. then use persp_mat to get
        #  orientation in stretched image. return orientation as a 2D vector


def get_window(track_img, car_pos, size):
    x = car_pos[0]
    y = car_pos[1]
    window = track_img[y-size:y+size, x-size: x+size]
    return window


if __name__ == '__main__':
    pass
    # for idx in range(len(drive_path)):
    #     live_screen = get_window(bev_track, drive_path[idx], 50)
    #     live_screen = cv2.resize(live_screen, (700, 700), interpolation=cv2.INTER_AREA)
    #     if idx-1 == -1:
    #         car_orientation = np.array(drive_path[idx+1]) - np.array(drive_path[idx])
    #     else:
    #         car_orientation = np.array(drive_path[idx]) - np.array(drive_path[idx-1])
    #     print(car_orientation)
    #     ang = 90 + math.degrees(math.atan2(car_orientation[1], car_orientation[0]))
    #     rot_mat = cv2.getRotationMatrix2D((350,350), ang, 1.0)
    #     print(rot_mat)
    #     live_screen = cv2.warpAffine(live_screen, rot_mat, (700, 700), cv2.INTER_NEAREST, cv2.BORDER_CONSTANT)
    #     cv2.imshow("img", live_screen)
    #     key_pressed = cv2.waitKey(0) & 0xFF
    #     if key_pressed == ord('q'):
    #         break
    # cv2.destroyAllWindows()
