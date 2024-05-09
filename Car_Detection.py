import cv2
import numpy as np
import os


class FrameProcessor:
    def __init__(self):
        self.counter = 0
        self.prev_x, self.prev_y, self.constant_radius, self.first_frame, _, self.lower_white, self.upper_white = self.initialize_tracking()
        self.prev_orientation = None
        self.ema_speeds = []
        self.ema_orientations = []
        self.ema_x = []
        self.ema_y = []


    def initialize_tracking(self):
        # Initialize with reasonable defaults or parameters
        return 0, 0, 25, True, 0, np.array([0, 0, 168], dtype=np.uint8), np.array([172, 111, 255], dtype=np.uint8)

    def process_single_frame(self, frame, frame_rate, scale_x, scale_y):

        # Process frame using detailed frame processing logic
        new_x, new_y, found, mask, contours, self.lower_white, self.upper_white = self.process_frame(frame,
                                                                                                     self.lower_white,
                                                                                                     self.upper_white,
                                                                                                     self.first_frame,
                                                                                                     self.prev_x,
                                                                                                     self.prev_y)

        if found:

            if not self.first_frame:
                dx, dy = self.calculate_deltas(self.prev_x, self.prev_y, new_x, new_y)
                speed, orientation = self.calculate_speed_and_orientation(dx, dy, scale_x, scale_y, frame_rate,
                                                                          self.prev_orientation)

                avg_speed = self.exponential_moving_average(self.ema_speeds, speed, alpha=0.2)  # Adjust alpha as needed
                avg_orientation = self.exponential_moving_average(self.ema_orientations, orientation, alpha=0.5)
                avg_x = self.exponential_moving_average(self.ema_x, new_x, alpha=0.1)
                avg_y = self.exponential_moving_average(self.ema_y, new_y, alpha=0.1)

                self.prev_x, self.prev_y = avg_x, avg_y  # Update the previous position

                return avg_x, avg_y, avg_speed, avg_orientation
            else:
                self.prev_x, self.prev_y = new_x, new_y
                self.first_frame = False
                return new_x, new_y, 0, 0  # No movement in the first frame
        return self.prev_x, self.prev_y, 0, self.prev_orientation if self.prev_orientation is not None else 0

    def process_frame(self, frame, lower_white, upper_white, first_frame, prev_x, prev_y):
        if first_frame:
            x_min, y_min, x_max, y_max = 0, 0, frame.shape[1], frame.shape[0]
        else:
            x_min, x_max, y_min, y_max = self.update_search_area(frame.shape, prev_x, prev_y)

        # Ensure indices are integers
        x_min, x_max, y_min, y_max = map(int, [x_min, x_max, y_min, y_max])

        cropped_frame = frame[y_min:y_max, x_min:x_max]
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        found, new_x, new_y = False, prev_x, prev_y
        if contours:
            c = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            new_x, new_y = int(x) + x_min, int(y) + y_min
            found = True

            # Convert x, y, and radius to integers for precise ROI calculation
            x, y, radius = int(x), int(y), int(radius)

            # Calculate bounds for ROI
            roi_x_min = max(0, x - int(radius * 0.6))
            roi_x_max = min(mask.shape[1], x + int(radius * 0.6))
            roi_y_min = max(0, y - int(radius * 0.6))
            roi_y_max = min(mask.shape[0], y + int(radius * 0.6))

            # Extract ROI from the mask and HSV image
            mask_roi = mask[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
            hsv_roi = hsv[roi_y_min:roi_y_max, roi_x_min:roi_x_max]

            # Calculate new HSV range based on the mean color within the inner part of the detected object
            mean_val = cv2.mean(hsv_roi, mask=mask_roi)
            lower_white = np.array([max(mean_val[0] - 20, 0), max(mean_val[1] - 60, 0), max(mean_val[2] - 50, 0)],
                                   dtype=np.uint8)
            upper_white = np.array([min(mean_val[0] + 20, 180), min(mean_val[1] + 50, 255), min(mean_val[2] + 50, 255)],
                                   dtype=np.uint8)

        return new_x, new_y, found, mask, contours, lower_white, upper_white

    def update_search_area(self, frame_shape, prev_x, prev_y, margin_scale=0.1):
        margin_x = int(frame_shape[1] * margin_scale)
        margin_y = int(frame_shape[0] * margin_scale)
        x_min = max(0, prev_x - margin_x)
        x_max = min(frame_shape[1], prev_x + margin_x)
        y_min = max(0, prev_y - margin_y)
        y_max = min(frame_shape[0], prev_y + margin_y)
        return x_min, x_max, y_min, y_max

    def calculate_roi_bounds(self, x, y, radius, mask_shape):
        # Ensure that ROI bounds are calculated as integers
        roi_x_min = max(0, int(x - int(radius * 0.6)))
        roi_x_max = min(mask_shape[1], int(x + int(radius * 0.6)))
        roi_y_min = max(0, int(y - int(radius * 0.6)))
        roi_y_max = min(mask_shape[0], int(y + int(radius * 0.6)))
        return roi_x_min, roi_x_max, roi_y_min, roi_y_max

    def calculate_deltas(self, prev_x, prev_y, new_x, new_y):
        return new_x - prev_x, new_y - prev_y

    def calculate_speed_and_orientation(self, dx, dy, scale_x, scale_y, frame_rate, prev_orientation, x=8):
        speed = np.sqrt((dx * scale_x) ** 2 + (dy * scale_y) ** 2) * frame_rate
        new_orientation = np.degrees(np.arctan2(dy * scale_y, dx * scale_x))

        # Adjust orientation to limit the change to x degrees
        if prev_orientation is not None:
            orientation_change = new_orientation - prev_orientation
            if orientation_change > x:
                new_orientation = prev_orientation + x
            elif orientation_change < -x:
                new_orientation = prev_orientation - x

        return speed, new_orientation

    def exponential_moving_average(self, values, new_value, alpha=0.8):

        if not values:
            # If the list is empty, initialize it with the new value
            values.append(new_value)
        else:

            # Calculate the EMA by applying the formula:
            # EMA_new = alpha * new_value + (1 - alpha) * EMA_old
            last_ema = values[-1]
            new_ema = alpha * new_value + (1 - alpha) * last_ema
            values.append(new_ema)
        return values[-1]


if __name__ == "__main__":
    pass
