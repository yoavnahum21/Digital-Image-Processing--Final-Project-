import numpy as np
import cv2


class Video_Read:
    def __init__(self, device_num):
        cv2.namedWindow("Digital image processing")
        self.vc = cv2.VideoCapture(device_num)

    def Read_video_from_live_cam(self) -> np.array: # יש מצב מחזיר משתנה אחר של cv2

        rval, frame = self.vc.read()
        if not rval:
            exit(1)
        return frame

    def Release_video(self) -> None:
        self.vc.release()
        cv2.destroyWindow("Digital Image Processing")

    def Current_Processed_frame() -> np.array: # יש מצב מחזיר משתנה אחר של cv2
        pass


# yoyo


