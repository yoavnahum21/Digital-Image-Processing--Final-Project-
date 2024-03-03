import cv2
from matplotlib import pyplot as plt

def image_show(frame):
    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow("Digital Image Processing", edges)
    cv2.waitKey(100)


