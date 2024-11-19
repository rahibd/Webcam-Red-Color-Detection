import cv2
import time
import numpy as np
import serial

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Use the USB webcam (0 is the default index for the first connected webcam)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

n_rows = 1
n_images_per_row = 6
color = (0, 0, 255) 
start_point = (0, 0)
end_point = (2112, 4608)
thickness = 15

# Function to send data over serial
def write_read(x):
    sam = "({co},w,18FF408F,100)".format(co=str(x))
    print(sam)
    ser.write(bytes(sam, 'utf-8'))
    time.sleep(0.06)

# Main loop for capturing and processing frames
while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    width = 1280
    height = 720
    roi_height = int(height / n_rows)
    roi_width = int(width / n_images_per_row)
    images = []
    count = 0

    # Split frame into sub-frames and process each for red color detection
    for x in range(n_rows):
        for y in range(n_images_per_row):
            count += 1
            tmp_image = frame[x * roi_height:(x + 1) * roi_height, y * roi_width:(y + 1) * roi_width]
            images.append(tmp_image)
            hsv_frame = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2HSV)
            
            # Define the red color range and create a mask
            low_red = np.array([161, 155, 84])
            high_red = np.array([179, 255, 255])
            red_mask = cv2.inRange(hsv_frame, low_red, high_red)
            red = cv2.bitwise_and(tmp_image, tmp_image, mask=red_mask)
            r = cv2.countNonZero(red_mask)

            # If red is detected, send serial data
            if r:
                if not ser.is_open:
                    ser.open()
                write_read(count)
                ser.close()

            # Draw rectangles on each sub-frame
            y1 = roi_width
            y2 = 0
            for x in range(n_rows):
                for y in range(n_images_per_row):
                    start_point = (y2, 0)
                    end_point = (y1, roi_height - 10)
                    y1 += roi_width
                    y2 += roi_width
                    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
            cv2.imshow('frame', frame)

    # Press ESC to exit
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
