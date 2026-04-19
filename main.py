import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

# 基準值初始化
baseline_diff = None 

print("啟動成功！")
print("請端正坐好，然後按 's' 鍵校準你的標準坐姿。")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1) # 鏡像處理
    h, w, _ = frame.shape
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        
        # 1. 獲取關鍵點座標 (像素座標)
        # 左耳(7), 右耳(8), 左肩(11), 右肩(12)
        l_ear = [lm[7].x * w, lm[7].y * h]
        r_ear = [lm[8].x * w, lm[8].y * h]
        l_shld = [lm[11].x * w, lm[11].y * h]
        r_shld = [lm[12].x * w, lm[12].y * h]

        # 2. 計算特徵值
        # 耳朵中點與肩膀中點的垂直距離
        ear_mid_y = (l_ear[1] + r_ear[1]) / 2
        shld_mid_y = (l_shld[1] + r_shld[1]) / 2
        curr_diff = shld_mid_y - ear_mid_y
        
        # 肩膀寬度（用來做歸一化，防止前後移動導致誤判）
        shld_width = math.sqrt((l_shld[0] - r_shld[0])**2 + (l_shld[1] - r_shld[1])**2)
        norm_diff = curr_diff / shld_width  # 得到的比例相對穩定

        # 3. 邏輯判斷
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            baseline_diff = norm_diff
            print(f"校準完成！基準值: {baseline_diff:.2f}")

        if baseline_diff is not None:
            # 如果當前比例低於基準值的 80%，判定為低頭或駝背
            if norm_diff < baseline_diff * 0.8:
                status = "BAD: Slumping!"
                color = (0, 0, 255)
                cv2.rectangle(image, (0,0), (w, h), (0,0,255), 10)
            else:
                status = "Good"
                color = (0, 255, 0)
            
            cv2.putText(image, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(image, f"Diff: {norm_diff:.2f} (Base: {baseline_diff:.2f})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(image, "Press 's' to Calibrate", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow('Improved Posture Checker', image)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
