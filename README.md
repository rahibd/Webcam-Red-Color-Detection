# Webcam-Red-Color-Detection

This Python project captures frames from a USB webcam, processes them for red color detection, and sends specific data over a serial connection if red pixels are detected. The program uses OpenCV for video capture and image processing, and the pyserial library for serial communication.

## Installation

### Required Libraries

To install the required libraries on a Linux-based system (such as Ubuntu), run the following commands:

1. **Install OpenCV (cv2)**  
   OpenCV is used for video capture and image manipulation.
   ```bash
   sudo apt update
   sudo apt install python3-opencv
2. **Install NumPy**:
  NumPy is used for numerical operations, especially for image processing.  

  sudo apt install python3-numpy  

4. **Install PySerial**:

PySerial is used for establishing a serial connection to a microcontroller or another device.

sudo apt install python3-serial  

4. **Final Setup**

After installing the system dependencies using apt, you may also need to install additional Python libraries (like OpenCV) using pip if not installed by apt. Here's how to do that:

pip3 install opencv-python numpy pyserial  
<br/>Serial Connection Setup:

The serial connection is initialized with the port /dev/ttyUSB0, a baud rate of 115200, and a timeout of 1 second. This allows the program to send and receive data via a serial interface.

### Methodology

The program captures video frames from a webcam (default index 0 for the first camera) at a resolution of 1280x720 pixels. The frame is split into sub-images based on the defined number of rows (n_rows) and columns (n_images_per_row), which are used to process smaller sections of the frame for red color detection. In this case, the frame is divided into 1 row with 6 sub-images.

Each sub-image is analyzed for the presence of red pixels using the HSV (Hue, Saturation, Value) color space. The red color is detected by defining a specific HSV range:

- **Low Red**: np.array(\[161, 155, 84\])
- **High Red**: np.array(\[179, 255, 255\])

A binary mask is created to isolate the red pixels, and the number of non-zero pixels is counted to determine if red is present in the sub-image. If red is detected, a serial message is sent with the sub-image index.

For visual feedback, rectangles are drawn around the detected areas in the original frame, and the updated frame is displayed. The program runs in a continuous loop, processing frames until the user presses the ESC key (ASCII code 27).

After the loop ends, the program releases the webcam and closes the OpenCV window. The sub-image processing allows for efficient parallel analysis, making the program sensitive to red-colored objects in the video feed. The serial communication could trigger actions on an external device, such as a microcontroller, based on the detection of red in any sub-image.  
Note:

Adjust the serial port (/dev/ttyUSB0) to match the connected device on your system.

Startup procedure:Procedure to Set Up the Python Script as a systemd Service on Raspberry Pi

Procedure to Set Up the Python Script as a systemd Service on Raspberry Pi  

1. Prepare Your Python Script

Make sure your Python script is fully functional and runs properly when executed manually.

&nbsp;  Test the Python script:

&nbsp;  Open a terminal and run:

/usr/bin/python3 /home/pi/Desktop/Red_Detection/Red_detection_webcam.py

&nbsp;  Confirm that the script opens the camera window and performs as expected.

1. Create the systemd Service File

&nbsp;  Create a new systemd service file for your script:

&nbsp;  Open a terminal and create the service file:

sudo nano /etc/systemd/system/red_detection.service

Add the following content to the service file:

\[Unit\]  
Description=Red Detection Webcam  
After=network.target

\[Service\]  
ExecStart=/usr/bin/python3 /home/pi/Desktop/Red_Detection/Red_detection_webcam.py  
WorkingDirectory=/home/pi/Desktop/Red_Detection  
Restart=always  
User=pi  
Group=pi  
Environment="DISPLAY=:0" # Specify the display for GUI  
Environment="XAUTHORITY=/home/pi/.Xauthority" # Specify the X authority file (optional)

\[Install\]  
WantedBy=multi-user.target

&nbsp;  Explanation:  
       Description: A short description of the service.  
       ExecStart: The command to execute your Python script.  
       WorkingDirectory: Ensures the script runs in the correct directory.  
       Restart=always: Ensures the script restarts if it crashes.  
       User=pi and Group=pi: Runs the service as the pi user.  
       Environment="DISPLAY=:0": Allows the service to access the graphical display (:0 is typically the default display on a Raspberry Pi).  
       Environment="XAUTHORITY=/home/pi/.Xauthority": Specifies the X authority file (this allows the script to access the X server, needed for GUI apps).

&nbsp;  Save and exit by pressing CTRL + X, then Y, and finally Enter.

1. Reload systemd and Enable the Service

&nbsp;  Reload systemd to recognize the new service file:

sudo systemctl daemon-reload

Enable the service to start on boot:

sudo systemctl enable red_detection.service

Start the service manually for the first time to test:

sudo systemctl start red_detection.service

Check the status to make sure it started successfully:

sudo systemctl status red_detection.service

If everything is set up correctly, it should show that the service is active and running. If there’s an issue, you can check the logs using:

journalctl -xeu red_detection.service

1. Reboot and Test

&nbsp;  Reboot your Raspberry Pi to ensure the script starts automatically on boot:

sudo reboot

After rebooting, the Python script should start automatically 30 seconds after boot, and the camera window should appear on the display.
