from Vid_Read import Video_Read
import comm_platform
import cv2

#main func
def main():
    camera_hands = Video_Read(0)
    port = comm_platform.init_port()
    comm_platform.Set_package_and_transmit('r', port)
    while True:
        signal = input()
        hands_frame = camera_hands.Read_video_from_live_cam()
        cv2.imshow("Digital Image Processing", hands_frame)
        cv2.waitKey(20)
        comm_platform.Set_package_and_transmit(signal, port)
        

if __name__ == '__main__':
    main()
