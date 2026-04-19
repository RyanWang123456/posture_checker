from ultralytics import YOLO

# Load the YOLO11 Nano pose model (ideal for edge devices)
model = YOLO("yolo11n-pose.pt")

# Run inference on an image, video, or webcam (source=0)
results = model(source="video.mp4", show=True, save=True)

# Process results
for result in results:
    keypoints = result.keypoints  # Access detected body joints
    print(keypoints.xy)          # Print x, y coordinates of keypoints

