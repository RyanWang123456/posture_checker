import torch
import cv2
import numpy as np
from picamzero import Camera
from lib.models.movenet_mobilenetv2 import MoveNet

# 1. Load Model
INPUT_SIZE = 192 
model = MoveNet(num_classes=17, width_mult=1.0)
state_dict = torch.load('movenet.pth', map_location='cpu')
model.load_state_dict(state_dict)
model.eval()

cam = Camera()

try:
    while True:
        # Capture frame (RGB)
        frame_rgb = cam.capture_array()
        h_orig, w_orig = frame_rgb.shape[:2]
        
        # Display frame in BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        # 2. Preprocess
        img_resized = cv2.resize(frame_rgb, (INPUT_SIZE, INPUT_SIZE))
        input_tensor = torch.from_numpy(img_resized).permute(2, 0, 1).float() / 255.0
        input_tensor = input_tensor.unsqueeze(0)

        # 3. Inference
        with torch.no_grad():
            output = model(input_tensor)
        
        # --- FIX: Extract tensor from list and reshape ---
        # The model returns a list [tensor], so we take index 0
        if isinstance(output, list):
            output = output[0]
            
        # Reshape the flattened 39168 values into 17 heatmaps of 48x48
        heatmaps = output.reshape(17, 48, 48).cpu().numpy()

        # 4. Find keypoints in heatmaps
        for i in range(17):
            heatmap = heatmaps[i]
            
            # Find the peak (max confidence) pixel in the 48x48 grid
            y_heat, x_heat = np.unravel_index(np.argmax(heatmap), heatmap.shape)
            confidence = heatmap[y_heat, x_heat]

            # Map from 48x48 heatmap back to original image size
            px = int((x_heat / 48.0) * w_orig)
            py = int((y_heat / 48.0) * h_orig)
            
            # Draw point if confidence is high enough
            if confidence > 0.2:
                cv2.circle(frame_bgr, (px, py), 5, (0, 255, 0), -1)

        # 5. Display
        cv2.imshow('MoveNet Pose', frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopped.")
finally:
    cv2.destroyAllWindows()

