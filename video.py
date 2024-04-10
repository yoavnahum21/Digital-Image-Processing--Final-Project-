import cv2
import numpy as np
from datetime import datetime
import os

def get_gray_mask(hsv_image):
    lower_gray = np.array([0, 0, 40])
    upper_gray = np.array([180, 50, 220])
    return cv2.inRange(hsv_image, lower_gray, upper_gray)

def get_blue_mask(hsv_image):
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    return cv2.inRange(hsv_image, lower_blue, upper_blue)

def scale_down_image(image, scale_percent=50):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def detect_path(hsv_image, min_width=5):
    gray_mask = get_gray_mask(hsv_image)
    kernel_size = int(min_width / 2)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    gray_mask_cleaned = cv2.morphologyEx(gray_mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(gray_mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = min_width * min_width
    return [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

def detect_car(hsv_image):
    blue_mask = get_blue_mask(hsv_image)
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    return None

def process_frame(frame, scale_percent=50):
    scaled_image = scale_down_image(frame, scale_percent)
    hsv_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2HSV)
    path_contours = detect_path(hsv_image)
    car_contour = detect_car(hsv_image)
    return create_simplified_image(scaled_image, path_contours, car_contour)

def create_simplified_image(image, path_contours, car_contour):
    simplified_image = 255 * np.ones_like(image)
    if path_contours:
        cv2.drawContours(simplified_image, path_contours, -1, (0, 0, 0), 3)
    if car_contour is not None:
        x, y, w, h = cv2.boundingRect(car_contour)
        center = (x + w // 2, y + h // 2)
        radius = 20
        cv2.circle(simplified_image, center, radius, (255, 0, 0), -1)

    return simplified_image


import time


def process_video(input_video_path, output_video_path, scale_percent=50):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale_percent / 100)
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale_percent / 100)
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    total_processing_time = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()  # Start timing the processing for this frame

        processed_frame = process_frame(frame, scale_percent)

        end_time = time.time()  # End timing after processing
        processing_time = end_time - start_time
        total_processing_time += processing_time

        out.write(processed_frame)

        frame_count += 1

    cap.release()
    out.release()

    print(f"Average processing time per frame: {total_processing_time / frame_count} seconds.")
    print(f"Total processing time: {total_processing_time} seconds for {frame_count} frames.")


# Example usage as before

# Example usage
input_video_path = 'blue_car_video.mp4'  # Update with the actual path to your video
output_video_path = 'blue_car_output_video.mp4'  # Update with the desired output path
process_video(input_video_path, output_video_path, scale_percent=50)
