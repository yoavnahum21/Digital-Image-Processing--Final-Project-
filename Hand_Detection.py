import cv2


class Player:
    def __init__(self, name, zero_pos, max_pos, min_pos):
        self.name = name
        self.zero_pos = zero_pos
        self.max_pos = max_pos
        self.min_pos = min_pos


if __name__ == '__main__':
    def image_show(frame):
        edges = cv2.Canny(frame, 100, 200)
        cv2.imshow("Digital Image Processing", edges)
        cv2.waitKey(100)
