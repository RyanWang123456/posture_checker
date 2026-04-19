import matplotlib.pyplot as plt
from picamzero import Camera
import time

# Initialize camera
cam = Camera()

# cam.start_preview()
cam.record_video("./video.mp4", duration=5)
# cam.stop_preview()
# Get the first frame to initialize the plot
# frame = cam.capture_array()

# try:
#     while True:
#         # Capture data directly into memory (no file saved)
#         frame = cam.capture_array()
#         print(frame.shape)
#         
# except KeyboardInterrupt:
#     print("Stopped.")


