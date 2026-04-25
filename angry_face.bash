# 顏色定義：紅色 (\x00\xf8)、黑色 (\x00\x00)
R='\x00\xf8'
B='\x00\x00'

while true; do
    # 1. 畫出紅色生氣臉 (64個像素)
    # 第一、二列：倒八字眉與空格
    # 第三、四列：眼睛
    # 第五列：空格
    # 第六列：憤怒的嘴巴
    (
      echo -en "$R$B$B$B$B$B$B$R" # row 0: 眉毛起頭
      echo -en "$B$R$R$B$B$R$R$B" # row 1: 眉毛向下傾斜
      echo -en "$B$B$B$R$R$B$B$B" # row 7: 空格
      echo -en "$B$R$B$B$B$B$R$B" # row 2: 眼睛
      echo -en "$B$R$B$B$B$B$R$B" # row 3: 眼睛
      echo -en "$B$B$B$B$B$B$B$B" # row 4: 空格
      echo -en "$B$B$R$R$R$R$B$B" # row 5: 嘴巴
      echo -en "$B$R$B$B$B$B$R$B" # row 6: 嘴巴邊角
    ) > /dev/fb1

    # 2. 持續顯示 2 秒
    sleep 2

    # 3. 初始化（全黑）
    dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
    
    # 4. 熄燈狀態持續 1 秒後再次循環
    sleep 1
done

