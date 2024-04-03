
import cv2
from Timer import Timer


if __name__ == '__main__':
    ext_camera = cv2.VideoCapture(1)
    dst_dir = "camera_test"
    img_counter = 0
    timer = Timer()
    timer.start()
    write = False
    while True:
        ret, frame = ext_camera.read()
        frame_time = timer.get_timer()
        filename = f"{dst_dir}/{frame_time}.png"
        if write:
            cv2.imwrite(filename, frame)
        cv2.imshow("feed", frame)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('r'):
            write = True
        if key_pressed == ord('q'):
            break
    ext_camera.release()
    cv2.destroyAllWindows()
