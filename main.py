from Vid_Read import Video_Read
import comm_platform
import cv2
import numpy as np
import matplotlib.pyplot as plt
camera_hands = Video_Read(0)


def calibration():
    count = 0
    while (True):
        frame = camera_hands.Read_video_from_live_cam()
        rect1_frame = cv2.rectangle(frame, (60, 140), (240, 340), (0, 255, 0), 4)
        rect2_frame = cv2.rectangle(rect1_frame, (400, 140), (580, 340), (0, 255, 0), 4)
        flipped_image = cv2.flip(rect2_frame, 1)
        left_hand = flipped_image[140:340, 60:240, :]
        right_hand = flipped_image[140:340, 400:580, :]
        cv2.imshow("rec_frame", flipped_image)
        count += 1
        cv2.waitKey(20)
        if count == 150:
            return left_hand, right_hand


# main func
def main():
    # port = comm_platform.init_port()
    # comm_platform.Set_package_and_transmit('r', port)
    # hands_frame = camera_hands.Read_video_from_live_cam()
    left_hand_ref, right_hand_ref = calibration()
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(left_hand_ref, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(right_hand_ref, cv2.COLOR_BGR2RGB))
    plt.show()
    while True:

        hands_frame = camera_hands.Read_video_from_live_cam()
        hands_frame = cv2.flip(hands_frame, 1)
        sift_left = cv2.SIFT_create()
        keypoints_left_reference, descriptors_left_reference = sift_left.detectAndCompute(left_hand_ref, None)
        keypoints_RT_left, descriptors_RT_left = sift_left.detectAndCompute(hands_frame, None)
        bf_left = cv2.BFMatcher() ## match between the photos
        matches = bf_left.match(descriptors_left_reference, descriptors_RT_left)
        good_matches = []
        for m in matches:
            if m.distance < 150: ## distance between features in RT and descriptor
                good_matches.append(m)

        matched_image_left = cv2.drawMatches(left_hand_ref, keypoints_left_reference, hands_frame, keypoints_RT_left,
                                        good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        cv2.imshow('Matched Keypoints', matched_image_left)
        cv2.waitKey(20)
        # ##########################
        # print("Enter your desired direction:")
        # signal = input()
        # # hands_frame = camera_hands.Read_video_from_live_cam()
        # cv2.imshow("rec_frame", hand_calibrate)
        # Show the image with keypoints
        # cv2.waitKey(20)
        # comm_platform.Set_package_and_transmit(signal, port)


if __name__ == '__main__':
    main()
