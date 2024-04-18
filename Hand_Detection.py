import cv2
from matplotlib import pyplot as plt
import numpy as np

''' This file contains the player class with the following attributes and methods:
1. name - self explanatory
2. get_curr_pos - reads camera frame and determines hand position.'''


class Player:
    def __init__(self, name, camera):
        self.name = name
        self.camera = camera
        self.result = None

    def calibration(self):
        count = 0
        while True:
            _, frame = self.camera.read()
            rect1_frame = cv2.rectangle(frame, (60, 140), (240, 340), (0, 255, 0), 4)
            cv2.rectangle(rect1_frame, (400, 140), (580, 340), (0, 255, 0), 4)

            flipped_image = cv2.flip(rect1_frame, 1)

            left_hand = flipped_image[140:340, 60:240, :]
            right_hand = flipped_image[140:340, 400:580, :]
            cv2.imshow("rec_frame", flipped_image)

            count += 1
            cv2.waitKey(20)

            if count == 100:
                concatenated_image = cv2.hconcat([left_hand, right_hand])
                concatenated_image_gray = cv2.cvtColor(concatenated_image,
                                                       cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication

                frame_check = cv2.cvtColor(concatenated_image, cv2.COLOR_BGR2HSV)

                frame_check_s = frame_check[:, :, 1]

                _, frame_check_s_masked = cv2.threshold(frame_check_s, 40, 255,
                                                        cv2.THRESH_BINARY)  ## to bitwise multiplication

                # Concatenate the images vertically
                concatenated_mult = np.vstack(
                    (cv2.bitwise_and(frame_check_s_masked, frame_check_s_masked), concatenated_image_gray))

                # Display or save the concatenated image
                cv2.imshow('these 2 to be multiplied Image', concatenated_mult)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                self.result = cv2.bitwise_and(frame_check_s_masked, concatenated_image_gray)
                return

    def sift(self):
        _, hands_frame = self.camera.read()
        frame_check_RT_gray = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2GRAY)  ## to bitwise multiplication

        frame_check_RT = cv2.cvtColor(hands_frame, cv2.COLOR_BGR2HSV)
        frame_check_RT_s = frame_check_RT[:, :, 1]

        _, frame_check_RT_s_masked = cv2.threshold(frame_check_RT_s, 40, 255,
                                                   cv2.THRESH_BINARY)  ## to bitwise multiplication

        result_RT = cv2.bitwise_and(frame_check_RT_gray, frame_check_RT_s_masked)

        hands_frame_RT = cv2.flip(result_RT, 1)

        sift = cv2.SIFT_create(nOctaveLayers=5, contrastThreshold=0.01, edgeThreshold=10, sigma=1.6)

        keypoints_reference, descriptors_reference = sift.detectAndCompute(self.result, None)  ## reference hands_frame

        keypoints_RT, descriptors_RT = sift.detectAndCompute(hands_frame_RT, None)  ## RT hands_frame

        matcher = cv2.BFMatcher()  # match between the photos
        if descriptors_RT is not None:
            matches = matcher.knnMatch(descriptors_reference, descriptors_RT, k=2)
            good_matches = []
            good_keypoints_x = []
            good_keypoints_y = []
            for m, n in matches:
                if m.distance < 0.71 * n.distance:
                    good_matches.append(m)
                    good_keypoints_x.append(round(keypoints_RT[m.trainIdx].pt[0]))
                    good_keypoints_y.append(round(keypoints_RT[m.trainIdx].pt[1]))
            hands_frame_RT = cv2.drawMatches(self.result, keypoints_reference, hands_frame_RT, keypoints_RT,
                                             good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        else:
            cv2.imshow('Matched Keypoints', hands_frame_RT)
            cv2.waitKey(20)
            return None

        cv2.imshow('Matched Keypoints', hands_frame_RT)
        cv2.waitKey(20)

        good_keypoints = list(zip(good_keypoints_y, good_keypoints_x))
        if len(good_matches) < 9:
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

        return slope



    def main():
        port = comm_platform.init_port()
        comm_platform.Set_package_and_transmit('r', port)
        result = calibration()

        while True:
            hands_frame = camera_hands.Read_video_from_live_cam()
            grad = sift(hands_frame, result)
            fsm(grad, port)

if __name__ == '__main__':
        main()