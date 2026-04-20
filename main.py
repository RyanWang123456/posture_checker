import cv2
import mediapipe as mp
import math
import time

# 初始化 MediaPipe (針對樹莓派使用 model_complexity=0)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 強制使用 V4L2 開啟相機
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 【關鍵優化】設定極低解析度，保證樹莓派能流暢運行
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 20)

baseline_diff = None 
bad_posture_start_time = None  # 計時器開始時間
alert_duration = 3  # 設定持續 3 秒才報警

print("啟動成功！請在樹莓派桌面環境下執行此腳本。")
print("請端正坐好，按 's' 鍵校準，按 'q' 退出。")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("讀取影格失敗")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # 轉為 RGB 供 MediaPipe 處理
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_image)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        
        # 獲取像素座標 (7:左耳, 8:右耳, 11:左肩, 12:右肩)
        ear_y = (lm[7].y + lm[8].y) / 2
        shld_y = (lm[11].y + lm[12].y) / 2
        
        # 計算特徵值：(肩膀Y - 耳朵Y) / 肩膀寬度
        curr_diff = shld_y - ear_y
        shld_width = math.sqrt((lm[11].x - lm[12].x)**2 + (lm[11].y - lm[12].y)**2)
        norm_diff = curr_diff / shld_width

        # 按 's' 校準
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            baseline_diff = norm_diff
            print(f"校準完成！基準比例: {baseline_diff:.2f}")

        if baseline_diff is not None:
            # 判斷是否坐姿不良 (低於基準值的 80%)
            if norm_diff < baseline_diff * 0.8:
                if bad_posture_start_time is None:
                    bad_posture_start_time = time.time()  # 開始計時
                
                elapsed_time = time.time() - bad_posture_start_time
                
                if elapsed_time >= alert_duration:
                    status = f"ALARM: SLUMPING ({int(elapsed_time)}s)"
                    color = (0, 0, 255)
                    cv2.rectangle(frame, (0,0), (w, h), (0,0,255), 10)
                else:
                    status = f"Warning: Detect Bad Posture ({int(elapsed_time)}s)"
                    color = (0, 165, 255) # 橘色
            else:
                status = "Good Posture"
                color = (0, 255, 0)
                bad_posture_start_time = None  # 恢復正常，重置計時器
            
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        else:
            cv2.putText(frame, "Press 's' to Calibrate", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # 顯示畫面
    cv2.imshow('RPi4 Posture Monitor', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
