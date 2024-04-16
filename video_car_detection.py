import cv2
import numpy as np


def open_video(filename):
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    return cap


def initialize_tracking():
    return None, None, 25, True, 0, np.array([0, 0, 168], dtype=np.uint8), np.array([172, 111, 255], dtype=np.uint8)


def update_search_area(frame_shape, prev_x, prev_y, margin_scale=0.1):
    margin_x = int(frame_shape[1] * margin_scale)
    margin_y = int(frame_shape[0] * margin_scale)
    x_min = max(0, prev_x - margin_x)
    x_max = min(frame_shape[1], prev_x + margin_x)
    y_min = max(0, prev_y - margin_y)
    y_max = min(frame_shape[0], prev_y + margin_y)
    return x_min, x_max, y_min, y_max


def process_frame(frame, lower_white, upper_white, first_frame, prev_x, prev_y):
    if first_frame:
        x_min, y_min, x_max, y_max = 0, 0, frame.shape[1], frame.shape[0]
    else:
        x_min, x_max, y_min, y_max = update_search_area(frame.shape, prev_x, prev_y)

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
        roi_x_min = max(0, x - int(radius * 0.7))
        roi_x_max = min(mask.shape[1], x + int(radius * 0.7))
        roi_y_min = max(0, y - int(radius * 0.7))
        roi_y_max = min(mask.shape[0], y + int(radius * 0.7))

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


def calculate_speed_and_orientation(prev_x, prev_y, new_x, new_y, scale_x, scale_y, frame_rate):
    dx = (new_x - prev_x) * scale_x
    dy = (new_y - prev_y) * scale_y
    speed = np.sqrt(dx ** 2 + dy ** 2) * frame_rate
    orientation = np.arctan2(dy, dx)
    return speed, orientation


def draw_orientation(frame, start, orientation, length_factor=50, color=(0, 255, 0)):
    end_x = int(start[0] + length_factor * np.cos(orientation))
    end_y = int(start[1] + length_factor * np.sin(orientation))
    cv2.arrowedLine(frame, start, (end_x, end_y), color, 3)


def main():
    cap = open_video('adjusted_output.avi')
    prev_x, prev_y, constant_radius, first_frame, frame_count, lower_white, upper_white = initialize_tracking()
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    scale_x, scale_y = 2.5 / cap.get(cv2.CAP_PROP_FRAME_WIDTH), 2 / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        new_x, new_y, found, mask, contours, lower_white, upper_white = process_frame(frame, lower_white, upper_white,
                                                                                      first_frame, prev_x, prev_y)
        if found and prev_x is not None and prev_y is not None:
            speed, orientation = calculate_speed_and_orientation(prev_x, prev_y, new_x, new_y, scale_x, scale_y,
                                                                 frame_rate)
            draw_orientation(frame, (prev_x, prev_y), orientation, 50, (0, 255, 0))
            cv2.putText(frame, f"Speed: {speed:.2f} m/s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if found:
            prev_x, prev_y = new_x, new_y

        cv2.circle(frame, (new_x, new_y), constant_radius, (0, 0, 255), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        first_frame = False

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
