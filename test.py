import cv2
import mediapipe as mp
import time

# 1. 先開啟相機
pipeline = "libcamerasrc ! video/x-raw, width=320, height=240 ! videoconvert ! appsink drop=True"
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

print("正在嘗試開啟視窗...")
model_loaded = False
pose = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 第 50 幀才載入 AI，確保視窗先出來
    if not model_loaded and cv2.waitKey(1) == -1: 
        # 顯示原始畫面，確認相機通了
        cv2.imshow('Posture Checker RPi4', frame)
        if time.process_time() > 3: # 執行 3 秒後再載入 AI
            print("正在載入 MediaPipe 模型...")
            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose(model_complexity=0)
            model_loaded = True

    if model_loaded:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_image)
        if results.pose_landmarks:
            cv2.putText(frame, "AI Active", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Posture Checker RPi4', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
