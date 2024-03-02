from Vid_Read import Video_Read
import comm_platform
import cv2


def main():
    camera_hands = Video_Read(0)
    while True:
        hands_frame = camera_hands.Read_video_from_live_cam()
        cv2.imshow("Digital Image Processing", hands_frame)
        # cv2.waitKey(20)
    

if __name__ == '__main__':
    main()

# check 12