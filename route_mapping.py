import cv2
import numpy as np
import datetime
import time


def apply_gaussian_blur(image, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def color_segmentation(image, lower_color, upper_color):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv_image, np.array(lower_color), np.array(upper_color))


def directional_morphology(mask, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


def close_gaps(mask, gap_size, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (gap_size, 1))
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


def remove_edge_pixels(image, edge_pct):
    h, w = image.shape[:2]
    edge_h, edge_w = int(edge_pct * h), int(edge_pct * w)
    image[:edge_h, :] = 255
    image[-edge_h:, :] = 255
    image[:, :edge_w] = 255
    image[:, -edge_w:] = 255
    return image


def detect_largest_red_shape(image, lower_red, upper_red):
    red_mask = color_segmentation(image, lower_red, upper_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea) if contours else None
    return largest_contour


def overlay_shape(image, shape):
    if shape is not None:
        cv2.drawContours(image, [shape], -1, (0, 0, 255), thickness=cv2.FILLED)


# def mark_route_points(image, shape):
#     peri = cv2.arcLength(shape, True)
#     approx = cv2.approxPolyDP(shape, 0.02 * peri, True)
#     points = [tuple(point[0]) for point in approx]
#     num_points = len(points)
#     step = max(num_points // 10,1)
#     print(f"{(0, num_points, step)}")
#     for i in range(0, num_points, step):
#         cv2.circle(image, points[i], 10, (255, 0, 0), -1)


def process_image(image_path, output_path, lower_yellow, upper_yellow, lower_red, upper_red, kernel_size, gap_size):
    start_time = time.time()

    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    red_shape = detect_largest_red_shape(image, lower_red, upper_red)
    blurred_image = apply_gaussian_blur(image, kernel_size)
    yellow_mask = color_segmentation(blurred_image, lower_yellow, upper_yellow)
    morphed_mask = directional_morphology(yellow_mask, kernel_size)
    gap_closed_mask = close_gaps(morphed_mask, gap_size, kernel_size)

    inverted_mask = cv2.bitwise_not(gap_closed_mask)
    filtered_image = remove_edge_pixels(inverted_mask, 0.04)

    final_image = cv2.merge([filtered_image] * 3)  # Convert to 3-channel image for color overlay
    overlay_shape(final_image, red_shape)
    # mark_route_points(final_image, red_shape)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    cv2.imwrite(f'{output_path}final_image_{timestamp}.jpg', final_image)

    print(f'Processing time: {time.time() - start_time:.2f} seconds')


# Define color ranges
lower_yellow = [15, 80, 0]
upper_yellow = [35, 255, 255]
lower_red = [0, 70, 50]
upper_red = [10, 255, 255]

# Kernel and gap sizes
kernel_size = 5
gap_size = 40

# Image paths
image_path = 'route_red_start_point.jpeg'
output_path = './'

# Process the image
process_image(image_path, output_path, lower_yellow, upper_yellow, lower_red, upper_red, kernel_size, gap_size)
