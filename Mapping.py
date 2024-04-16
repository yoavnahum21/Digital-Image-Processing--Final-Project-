""" This file contains the class track designed to hold the track object with the following attributes and methods:
1.

"""
import cv2
import numpy as np


class Track:
    def __init__(self, camera):
        self.origin_img = None
        self.bev_track = None
        self.start_point = None
        self.track_cam = camera
        self.persp_mat = None

    def get_track_img(self) -> None:
        while True:
            _, frame = self.track_cam.read()
            cv2.imshow("track cam", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                break
        self.origin_img = frame
        self.track_cam.release()
        cv2.destroyAllWindows()

    def get_bev_track(self):
        hsv_img = cv2.cvtColor(self.origin_img, cv2.COLOR_BGR2HSV)
        _, v_threshed = cv2.threshold(hsv_img[:, :, 2], 200, 255, cv2.THRESH_BINARY)
        _, s_threshed = cv2.threshold(hsv_img[:, :, 1], 160, 255, cv2.THRESH_BINARY)
        corner_img = cv2.bitwise_and(s_threshed, v_threshed)
        corners = np.float32(np.array(get_corner_points(corner_img)))
        dest_corners = np.float32([[0, 0], [639, 0], [0, 479], [639, 479]])
        persp_mat = cv2.getPerspectiveTransform(corners, dest_corners)
        bev_track = cv2.warpPerspective(self.origin_img, persp_mat, (640, 480))
        #bev_track = cv2.cvtColor(bev_track, cv2.COLOR_BGR2HSV)
        cv2.imshow("b", bev_track[:,:,0])
        cv2.waitKey(0)
        cv2.imshow("g", bev_track[:,:,1])
        cv2.waitKey(0)
        cv2.imshow("r", bev_track[:,:,2])
        cv2.waitKey(0)
        _, v_threshed1 = cv2.threshold(bev_track[:, :, 1], 130, 255, cv2.THRESH_BINARY)
        v_threshed1 = cv2.erode(bev_track, kernel=np.array([[1, 1], [1, 1]]), iterations=3)
        cv2.imshow("bev1", v_threshed1)
        cv2.waitKey(0)
        bev_track = cv2.bitwise_and(v_threshed, s_threshed)
        bev_track = cv2.copyMakeBorder(bev_track, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        bev_track = cv2.dilate(bev_track, kernel=np.array([[1, 1], [1, 1]]), iterations=20)
        self.bev_track = cv2.Canny(bev_track, 0, 100)

    def get_starting_pos(self):
        pass


def get_corner_points(img):
    top_left = (320, 240)
    top_right = (320, 240)
    bot_left = (320, 240)
    bot_right = (320, 240)
    ys, xs = np.shape(img)
    for y in range(ys):
        for x in range(xs):
            if img[y, x] == 255:
                if x <= top_left[0] and y <= top_left[1]:
                    top_left = (x, y)
                elif x >= top_right[0] and y <= top_right[1]:
                    top_right = (x, y)
                elif x <= bot_left[0] and y >= bot_left[1]:
                    bot_left = (x, y)
                elif x >= bot_right[0] and y >= bot_right[1]:
                    bot_right = (x, y)
    return [top_left, top_right, bot_left, bot_right]


if __name__ == "__main__":
    pass

    # img = cv2.imread("camera_test/13.562_real.png")
    # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # _, v_threshed = cv2.threshold(img[:, :, 2], 200, 255, cv2.THRESH_BINARY)
    # cv2.imshow("v threshed", v_threshed)
    # cv2.waitKey(0)
    # _, s_threshed = cv2.threshold(hsv_img[:, :, 1], 160, 255, cv2.THRESH_BINARY)
    # cv2.imshow("s", s_threshed)
    # cv2.waitKey(0)
    # corner_img = cv2.bitwise_and(s_threshed, v_threshed)
    # cv2.imshow("corners", corner_img)
    # cv2.waitKey(0)
    # _, corner_img = cv2.threshold(ref_img[:, :, 0], 160, 255, cv2.THRESH_BINARY)
    # cv2.imshow("corner", corner_img)
    # cv2.waitKey(0)
    # corners = np.float32(np.array(get_corner_points(corner_img)))
    # dest_corners = np.float32([[0, 0], [639, 0], [0, 479], [639, 479]])
    # persp_mat = cv2.getPerspectiveTransform(corners, dest_corners)
    # bev_track = cv2.warpPerspective(img, persp_mat, (640, 480))
    # bev_track = cv2.cvtColor(bev_track, cv2.COLOR_BGR2LAB)
    # _, bev_track = cv2.threshold(bev_track[:, :, 2], 210, 255, cv2.THRESH_BINARY)
    # bev_track = cv2.dilate(bev_track, kernel=np.array([[1, 1], [1, 1]]), iterations=20)
    # bev_track = cv2.Canny(bev_track, 0, 100)
    # bev_track = cv2.copyMakeBorder(bev_track, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
