import cv2
import mediapipe as mp
import math
import time
import numpy as np
import subprocess
import os

# 1. 強制設定樹莓派顯示環境
os.environ["DISPLAY"] = ":0"

# 2. 初始化 MediaPipe (model_complexity=0 是樹莓派流暢的關鍵)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 3. 樹莓派專用 GStreamer 管道 (代替 cap = cv2.VideoCapture)
W, H = 320, 240
gst_cmd = [
    'gst-launch-1.0', 'libcamerasrc', '!', 
    f'video/x-raw,width={W},height={H},framerate=15/1', '!', 
    'videoconvert', '!', 'video/x-raw,format=BGR', '!', 
    'fdsink'
]
proc = subprocess.Popen(gst_cmd, stdout=subprocess.PIPE, bufsize=10**8)

# 變數初始化
baseline_diff = None 
bad_posture_start_time = None  
alert_duration = 3  
frame_size = W * H * 3

print("啟動成功！")
print("請端正坐好，按 's' 鍵校準，按 'q' 退出。")

try:
    while True:
        # 從系統管道讀取影像數據
        raw_frame = proc.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            continue

        # 轉換為 NumPy 格式並加上 .copy() 確保可寫入
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((H, W, 3)).copy()
        
        # 樹莓派建議不翻轉以節省 CPU，如需鏡像再加這行: frame = cv2.flip(frame, 1)
        
        # 轉為 RGB 供 MediaPipe 處理
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_image)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            
            # 獲取座標 (7:左耳, 8:右耳, 11:左肩, 12:右肩)
            ear_y = (lm[7].y + lm[8].y) / 2
            shld_y = (lm[11].y + lm[12].y) / 2
            
            # 計算比例：(肩膀Y - 耳朵Y) / 肩膀寬度 (歸一化防止前後移動誤判)
            curr_diff = shld_y - ear_y
            shld_width = math.sqrt((lm[11].x - lm[12].x)**2 + (lm[11].y - lm[12].y)**2)
            
            if shld_width > 0:
                norm_diff = curr_diff / shld_width
            else:
                norm_diff = 0

            if baseline_diff is not None:
                # 判定邏輯 (低於基準 80%)
                if norm_diff < baseline_diff * 0.8:
                    if bad_posture_start_time is None:
                        bad_posture_start_time = time.time()
                    
                    elapsed = time.time() - bad_posture_start_time
                    # WARNING
                    if elapsed >= alert_duration:
                        status = f"ALARM: SLUMPING ({int(elapsed)}s)"
                        color = (0, 0, 255)
                        cv2.rectangle(frame, (0,0), (W, H), (0,0,255), 10)

                        # send warning request to llm
                        print("SIGNAL:WARNING", flush=True)
                        

                    
                    else:
                        status = f"Warning... ({int(elapsed)}s)"
                        color = (0, 165, 255)

                else:
                    status = "Good Posture"
                    color = (0, 255, 0)
                    bad_posture_start_time = None
                
                cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            else:
                cv2.putText(frame, "Press 's' to Calibrate", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # 顯示畫面
        cv2.imshow('RPi4 Posture Monitor', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            baseline_diff = norm_diff
            print(f"校準完成！基準比例: {baseline_diff:.2f}")
        elif key == ord('q'):
            break

finally:
    proc.terminate()
    cv2.destroyAllWindows()
