import subprocess
import time
import os

class SenseAnimation:
    def __init__(self):
        self.current_process = None

    def _cleanup_led(self):
        """私有函數：強制清空 LED 矩陣"""
        subprocess.run("dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null", shell=True)

    def start_loading(self, file_path):
        """
        啟動循環動畫 (loading1.bash 或 loading2.bash)
        """
        # 如果已有動畫在執行，先停止它
        self.stop_loading()
        
        if os.path.exists(file_path):
            # 使用 Popen 在背景執行 bash 檔案
            self.current_process = subprocess.Popen(['/bin/bash', file_path])
            print(f"Started animation: {file_path}")
        else:
            print(f"Error: {file_path} not found.")

    def stop_loading(self):
        """
        停止當前運行的動畫並清理 LED
        """
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate() # 發送停止訊號
            self.current_process.wait()      # 等待進程完全結束
            self.current_process = None
            print("Animation stopped.")
        
        self._cleanup_led()

    def play_middle_finger(self, file_path):
        """
        播放一次性動畫 (middle_finger.bash)，該腳本內建 2 秒後自動清理
        """
        # 播放前先清理目前的動畫
        self.stop_loading()

        if os.path.exists(file_path):
            # run 會等待指令執行完畢 (因為腳本裡有 sleep 2)
            subprocess.run(['/bin/bash', file_path])
            print(f"Played one-time animation: {file_path}")
        else:
            print(f"Error: {file_path} not found.")

# --- 使用範例 ---
if __name__ == "__main__":
    anim = SenseAnimation()

    # 1. 測試 Loading 動畫
    anim.start_loading("./loading1.bash")
    time.sleep(5)  # 讓它跑 5 秒
    anim.stop_loading()

    anim.start_loading("./loading2.bash")
    time.sleep(5)
    anim.stop_loading()

    time.sleep(1)

    # 2. 測試 Middle Finger (自動播放 2 秒並退出)
    anim.play_middle_finger("./middle_finger.bash")

