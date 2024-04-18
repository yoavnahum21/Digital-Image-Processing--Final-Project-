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
        self.corner_list = []

    def get_track_img(self) -> None:
        while True:
            _, frame = self.track_cam.read()
            cv2.imshow("track cam", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                break
        self.origin_img = frame
        # self.track_cam.release()
        cv2.destroyAllWindows()

    def get_bev_track(self):
        corners = np.float32([[145, 85], [508, 65], [50, 440], [573, 439]])
        dest_corners = np.float32([[0, 0], [639, 0], [0, 479], [639, 479]])
        self.persp_mat = cv2.getPerspectiveTransform(corners, dest_corners)
        bev_track = cv2.warpPerspective(self.origin_img, self.persp_mat, (640, 480))
        _, bev_comb = cv2.threshold(bev_track[:, :, 1], 120, 255, cv2.THRESH_BINARY)
        bev_track = cv2.cvtColor(bev_track, cv2.COLOR_BGR2LAB)
        _, a_thresh = cv2.threshold(bev_track[:, :, 1], 160, 255, cv2.THRESH_BINARY)
        a_thresh = cv2.dilate(a_thresh, kernel=np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), iterations=60)
        bev_clean = np.maximum(bev_comb - a_thresh, 0)
        cv2.imshow("bev_clean", bev_clean)
        cv2.waitKey(2)
        # self.get_harris_corners(bev_clean)
        bev_clean = cv2.copyMakeBorder(bev_clean, 70, 70, 70, 70, cv2.BORDER_CONSTANT)
        bev_clean = cv2.dilate(bev_clean, kernel=np.array([[1, 1], [1, 1]]), iterations=20)
        self.bev_track = cv2.Canny(bev_clean, 0, 100)

    def get_harris_corners(self, bin_img):
        bin_img = cv2.dilate(bin_img, kernel=np.array([[1, 1], [1, 1]]), iterations=10)
        blocksize = 5  # Neighborhood size for computing corners
        ksize = 5  # Aperture parameter for Sobel derivative
        k = 0.04  # Harris detector free parameter

        # Detect corners using cv2.cornerHarris
        harris_resp = cv2.cornerHarris(bin_img, blocksize, ksize, k)
        max_resp = np.max(harris_resp)
        harris_thresh = 0.05 * max_resp
        _, harris_resp = cv2.threshold(harris_resp, harris_thresh, 255, cv2.THRESH_BINARY)
        cv2.imshow("resp", harris_resp)
        cv2.waitKey(0)
        non_ref_corners = np.where(harris_resp == 255)
        for idx in range(len(non_ref_corners[0])):
            x = non_ref_corners[1][idx]
            y = non_ref_corners[0][idx]
            self.corner_list.append(np.array([y, x]))



def dist(v1,v2):
    return np.sqrt(np.sum((v2 - v1) ** 2))
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
