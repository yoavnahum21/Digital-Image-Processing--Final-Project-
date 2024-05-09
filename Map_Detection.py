""" This file contains the class track designed to hold the track object with the following attributes and methods:
1.

"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

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
        cv2.destroyAllWindows()

    def get_bev_track(self):
        corners = np.float32([[145, 85], [508, 65], [50, 440], [573, 439]])
        dest_corners = np.float32([[0, 0], [639, 0], [0, 479], [639, 479]])
        self.persp_mat = cv2.getPerspectiveTransform(corners, dest_corners)
        bev_track = cv2.warpPerspective(self.origin_img, self.persp_mat, (640, 480))
        bev_track = cv2.cvtColor(bev_track, cv2.COLOR_BGR2LAB)
        hist = cv2.calcHist([bev_track[:,:,0]], [0], None, [256], [0, 256])
        _, bev_clean = cv2.threshold(bev_track[:, :, 0], 100, 255, cv2.THRESH_BINARY)
        cv2.imshow('clean', bev_clean)
        cv2.waitKey(0)
        self.get_harris_corners(bev_clean)
        bev_clean = cv2.copyMakeBorder(bev_clean, 70, 70, 70, 70, cv2.BORDER_CONSTANT)
        bev_clean = cv2.dilate(bev_clean, kernel=np.array([[1, 1], [1, 1]]), iterations=20)
        self.bev_track = cv2.Canny(bev_clean, 0, 100)
        for corner in self.corner_list:
            cv2.circle(self.bev_track, corner + [70, 70], 30, 128, 3)

    def get_harris_corners(self, bin_img):
        bin_img = cv2.dilate(bin_img, kernel=np.array([[1, 1], [1, 1]]), iterations=7)
        blocksize = 5
        ksize = 5
        k = 0.05
        harris_resp = cv2.cornerHarris(bin_img, blocksize, ksize, k)
        harris_resp = cv2.erode(harris_resp, kernel=np.array([[1, 1], [1, 1]]), iterations=2)
        max_resp = np.max(harris_resp)
        harris_thresh = 0.1 * max_resp
        _, harris_resp = cv2.threshold(harris_resp, harris_thresh, 255, cv2.THRESH_BINARY)
        non_ref_corners = np.where(harris_resp == 255)
        for idx in range(len(non_ref_corners[0])):
            x = non_ref_corners[0][idx]
            y = non_ref_corners[1][idx]
            self.corner_list.append(np.array([y, x]))
        self.corner_list = self.refine_corners(150)

    def refine_corners(self, dist_threshold):
        corners = [self.corner_list[0]]
        for point in self.corner_list:
            check = True
            for corn in corners:
                if dist(point, corn) < dist_threshold:
                    check = False
            if check:
                corners.append(point)
        return corners


def dist(point1, point2):
    distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5
    return distance



if __name__ == "__main__":
    pass
