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

        flipped_image = cv2.flip(rect1_frame, 1)

        left_hand = flipped_image[140:340, 60:240, :]
        right_hand = flipped_image[140:340, 400:580, :]
        cv2.imshow("rec_frame", flipped_image)

        count += 1
        cv2.waitKey(20)
        if count == 100:
            return left_hand, right_hand

def sift(hands_frame, result):
    frame_check_RT_gray = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication

    frame_check_RT = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2HSV)
    frame_check_RT_h = frame_check_RT[:, :, 0]
    frame_check_RT_s = frame_check_RT[:, :, 1]

    _, frame_check_RT_s_masked = cv2.threshold(frame_check_RT_s, 40, 255,
                                               cv2.THRESH_BINARY)  ## to bitwise multiplication

    result_RT = cv2.bitwise_and(frame_check_RT_gray, frame_check_RT_s_masked)

    hands_frame_RT = cv2.flip(result_RT, 1)

    sift = cv2.SIFT_create(nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)
    sift.setEdgeThreshold(1000)

    keypoints_reference, descriptors_reference = sift.detectAndCompute(result, None)  ## reference hands_frame

    keypoints_RT, descriptors_RT = sift.detectAndCompute(hands_frame_RT, None)  ## RT hands_frame

    matcher = cv2.BFMatcher()  # match between the photos
    if descriptors_RT is not None:
        matches = matcher.knnMatch(descriptors_reference, descriptors_RT, k=2)
        good_matches = []
        good_keypoints_x = []
        good_keypoints_y = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
                good_keypoints_x.append(round(keypoints_RT[m.trainIdx].pt[0]))
                good_keypoints_y.append(round(keypoints_RT[m.trainIdx].pt[1]))
        hands_frame_RT = cv2.drawMatches(result, keypoints_reference, hands_frame_RT, keypoints_RT,
                                             good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    else:
        cv2.imshow('Matched Keypoints', hands_frame_RT)
        cv2.waitKey(20)
        return None

    cv2.imshow('Matched Keypoints', hands_frame_RT)
    cv2.waitKey(20)

    good_keypoints = list(zip(good_keypoints_y, good_keypoints_x))
    if len(good_matches) < 6:
        cv2.imshow('Matched Keypoints', hands_frame_RT)
        cv2.waitKey(20)
        return None
    left_good_keypoints = [left for left in good_keypoints if left[1] < 280]
    right_good_keypoints = [right for right in good_keypoints if right[1] >= 360]

    first_elements_left_x = [item[0] for item in left_good_keypoints]
    first_elements_left_y = [item[1] for item in left_good_keypoints]

    first_elements_right_x = [item[0] for item in right_good_keypoints]
    first_elements_right_y = [item[1] for item in right_good_keypoints]

    if len(left_good_keypoints) == 0 or len(right_good_keypoints) == 0:
        cv2.imshow('Matched Keypoints', hands_frame_RT)
        cv2.waitKey(20)
        return None

    else:
        centroid_left_x = sum(first_elements_left_x) // len(left_good_keypoints)
        centroid_left_y = sum(first_elements_left_y) // len(left_good_keypoints)

        centroid_right_x = sum(first_elements_right_x) // len(right_good_keypoints)
        centroid_right_y = sum(first_elements_right_y) // len(right_good_keypoints)

    centroid_left = (centroid_left_y + 360, centroid_left_x)
    centroid_right = (centroid_right_y + 360, centroid_right_x)

    cv2.line(hands_frame_RT, centroid_left, centroid_right, (0, 255, 0), 3)
    cv2.imshow('Matched Keypoints', hands_frame_RT)
    cv2.waitKey(20)

    slope = -(centroid_right[1] - centroid_left[1]) / (centroid_right[0] - centroid_left[0])

    print("Slope of the line:", slope)
    return  slope



def fsm(grad, port):

    if grad is None:
        comm_platform.Set_package_and_transmit('r', port) # stop car
    elif (grad <= 0.2) and (grad >= -0.2):
        comm_platform.Set_package_and_transmit('w', port) # go forward
    elif (grad < -0.2) and (grad >= -0.5):
        comm_platform.Set_package_and_transmit('y', port) # go forward and right
    elif (grad > 0.2) and (grad <= 0.5):
        comm_platform.Set_package_and_transmit('t', port) # go forward and left
    elif grad > 0.5:
        comm_platform.Set_package_and_transmit('a', port)  # go right
    elif grad < -0.5:
        comm_platform.Set_package_and_transmit('d', port)  # go right
    else:
        return
    cv2.waitKey(50)
    comm_platform.Set_package_and_transmit('r', port)
    return


# main func
def main():
    port = comm_platform.init_port()
    comm_platform.Set_package_and_transmit('r', port)
    left_hand_ref, right_hand_ref = calibration()

    concatenated_image = cv2.hconcat([left_hand_ref, right_hand_ref])
    concatenated_image_gray = cv2.cvtColor(concatenated_image, cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication
    cv2.imshow('concatenated_image_gray', concatenated_image_gray)
    cv2.waitKey(0)

    frame_check = cv2.cvtColor(concatenated_image, cv2.COLOR_BGR2HSV)

    frame_check_s = frame_check[:, :, 1]
    cv2.imshow('HSV Image ssss', frame_check_s)
    cv2.waitKey(0)

    _, frame_check_s_masked = cv2.threshold(frame_check_s, 40, 255, cv2.THRESH_BINARY)  ## to bitwise multiplication

    cv2.imshow('channel s mask', frame_check_s_masked)
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

    # sift = cv2.SIFT_create(nfeatures=100, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)
    # sift.setEdgeThreshold(1000)
    #
    # keypoints_reference, descriptors_reference = sift.detectAndCompute(result, None)  ## reference hands_frame
    #
    # imgKp1 = cv2.drawKeypoints(result, keypoints_reference,None)
    # cv2.imshow('imgkp1', imgKp1)
    # cv2.waitKey(0)
    #
    # keypoint_locations = []
    #
    # for keypoint in keypoints_reference:
    #     x, y = keypoint.pt  # Get the (x, y) coordinates of the keypoint
    #     x = round(x)
    #     y = round(y)
    #     keypoint_locations.append((x, y))  # Append the coordinates to the list
    #
    # print("Keypoint Locations:", keypoint_locations)
    #
    #


    while True:

        hands_frame = camera_hands.Read_video_from_live_cam()
        grad = sift(hands_frame, result)
        fsm(grad,port)





    #     # print("Enter your desired direction:")
    #     # signal = input()
    #     # # hands_frame = camera_hands.Read_video_from_live_cam()
    #     # cv2.imshow("rec_frame", hand_calibrate)
    #     # Show the image with keypoints
    #     # cv2.waitKey(20)
    #     # comm_platform.Set_package_and_transmit(signal, port)


if __name__ == '__main__':
    main()