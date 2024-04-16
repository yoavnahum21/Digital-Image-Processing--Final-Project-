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
        # rect1_frame = cv2.circle(rect2_frame,(490,240), 80,(255,0,0),2)

        flipped_image = cv2.flip(rect1_frame, 1)

        left_hand = flipped_image[140:340, 60:240, :]
        right_hand = flipped_image[140:340, 400:580, :]
        left_hand_gauss = cv2.GaussianBlur(left_hand, ksize=(3, 3), sigmaX=0)
        right_hand_gauss = cv2.GaussianBlur(right_hand, ksize=(3, 3), sigmaX=0)
        cv2.imshow("rec_frame", flipped_image)

        count += 1
        cv2.waitKey(20)
        if count == 100:
            return left_hand, right_hand


# main func
def main():
    # port = comm_platform.init_port()
    # comm_platform.Set_package_and_transmit('r', port)
    hands_frame = camera_hands.Read_video_from_live_cam()
    left_hand_ref, right_hand_ref = calibration()

    concatenated_image = cv2.hconcat([left_hand_ref, right_hand_ref])
    concatenated_image_gray = cv2.cvtColor(concatenated_image, cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication
    cv2.imshow('concatenated_image_gray', concatenated_image_gray)
    cv2.waitKey(0)

    frame_check = cv2.cvtColor(concatenated_image, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image ', frame_check)
    cv2.waitKey(0)

    frame_check_s = frame_check[:, :, 1]
    cv2.imshow('HSV Image ssss', frame_check_s)
    cv2.waitKey(0)

    frame_check_h = 255 - frame_check[:, :, 2]
    cv2.imshow('HSV Image vvvv', frame_check_h)
    cv2.waitKey(0)

    # plt.figure(figsize=(8, 12))
    # histogram_h = cv2.calcHist([frame_check_h], [0], None, [256], [0, 256])
    # histogram_s = cv2.calcHist([frame_check_s], [0], None, [256], [0, 256])
    #
    #
    # # Plot S channel histogram
    # plt.subplot(2, 1, 1)
    # plt.plot(histogram_s, color='blue')
    # plt.title('Histogram of S (Saturation) Channel')
    # plt.xlabel('S Value')
    # plt.ylabel('Frequency')
    # plt.grid(True)
    #
    # # Plot H channel histogram
    # plt.subplot(2, 1, 2)
    # plt.plot(histogram_h, color='green')  # Using green color for H channel
    # plt.title('Histogram of H (Hue) Channel')
    # plt.xlabel('H Value')
    # plt.ylabel('Frequency')
    # plt.grid(True)
    #
    # plt.tight_layout()  # Adjust layout for better spacing
    # plt.show() ## histograms

    # _, frame_check_s = cv2.threshold(frame_check_s, 40, 130, cv2.THRESH_BINARY)
    _, frame_check_s_masked = cv2.threshold(frame_check_s, 40, 255, cv2.THRESH_BINARY)  ## to bitwise multiplication

    cv2.imshow('channel s mask', frame_check_s_masked)
    cv2.waitKey(0)

    # _, frame_check_h = cv2.threshold(frame_check_h, 20, 60, cv2.THRESH_BINARY)
    _, frame_check_h_masked = cv2.threshold(frame_check_h, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow('channel h mask', frame_check_h_masked)
    cv2.waitKey(0)

    # Concatenate the images vertically
    concatenated_mult = np.vstack(
        (cv2.bitwise_and(frame_check_s_masked, frame_check_s_masked), concatenated_image_gray))

    # Display or save the concatenated image
    cv2.imshow('these 2 to be multiplied Image', concatenated_mult)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    result = cv2.bitwise_and(frame_check_s_masked, concatenated_image_gray)
    cv2.imshow('result', result)
    cv2.waitKey(0)

    while True:

        hands_frame = camera_hands.Read_video_from_live_cam()
        hands_frame = cv2.rectangle(hands_frame, (200, 0), (480, 480), (0, 255, 0), 4)

        frame_check_RT_gray = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication

        frame_check_RT = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2HSV)
        frame_check_RT_h = frame_check_RT[:, :, 0]
        frame_check_RT_s = frame_check_RT[:, :, 1]

        _, frame_check_RT_s = cv2.threshold(frame_check_RT_s, 40, 130, cv2.THRESH_BINARY)
        _, frame_check_RT_s_masked = cv2.threshold(frame_check_RT_s, 40, 255,
                                                   cv2.THRESH_BINARY)  ## to bitwise multiplication

        _, frame_check_RT_h_masked = cv2.threshold(frame_check_RT_h, 30, 255, cv2.THRESH_BINARY_INV)

        result_RT = cv2.bitwise_and(frame_check_RT_gray, frame_check_RT_s_masked)

        hands_frame_RT = cv2.flip(result_RT, 1)
        #
        # x1, y1 = 200, 200  # Top-left corner
        # x2, y2 = 400, 400  # Bottom-right corner
        #
        # black_rect = np.zeros_like(hands_frame_RT)
        #
        # # Draw a white rectangle on the black image to create the mask
        # cv2.rectangle(black_rect, (x1, y1), (x2, y2), (255, 255, 255), -1)
        #
        # # Use the bitwise NOT operation to invert the mask (black becomes white, white becomes black)
        # mask = cv2.bitwise_not(black_rect)
        #
        # # Use the bitwise AND operation to combine the mask with the original image
        # hands_frame_RT = cv2.bitwise_and(hands_frame_RT, mask)

        sift = cv2.SIFT_create()
        sift.setEdgeThreshold(1000)

        keypoints_reference, descriptors_reference = sift.detectAndCompute(result, None)  ## reference hands_frame

        # mask = np.ones_like(hands_frame_RT, dtype=np.uint8) * 255  # Initialize with all white
        # mask[0:500, 200:500] = 0

        keypoints_RT, descriptors_RT = sift.detectAndCompute(hands_frame_RT, None)  ## RT hands_frame

        matcher = cv2.BFMatcher()  # match between the photos
        if descriptors_RT is not None:
            matches = matcher.knnMatch(descriptors_reference, descriptors_RT, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
            matched_image_left = cv2.drawMatches(result, keypoints_reference, hands_frame_RT, keypoints_RT,
                                                 good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        cv2.imshow('Matched Keypoints', matched_image_left)
        # cv2.imshow('imgKp1',imgKp1)
        # cv2.imshow('imgKp2', imgKp2)
        cv2.waitKey(20)
        #
        print(len(good_matches))

    #
    #
    #     # print (descriptors_reference.shape, descriptors_RT.shape)
    #     # print( len(good_matches))
    #     # # ##########################
    #     # print("Enter your desired direction:")
    #     # signal = input()
    #     # # hands_frame = camera_hands.Read_video_from_live_cam()
    #     # cv2.imshow("rec_frame", hand_calibrate)
    #     # Show the image with keypoints
    #     # cv2.waitKey(20)
    #     # comm_platform.Set_package_and_transmit(signal, port)


if __name__ == '__main__':
    main()
