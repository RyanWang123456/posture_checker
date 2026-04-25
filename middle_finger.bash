# 顏色定義：紅色 (\x00\xf8)、黑色 (\x00\x00)
R='\x00\xf8'
B='\x00\x00'

# 繪製紅色的中指圖案
(
  echo -en "$B$B$B$R$R$B$B$B" # Row 0: 中指指尖
  echo -en "$B$B$B$R$R$B$B$B" # Row 1: 中指
  echo -en "$B$B$B$R$R$B$B$B" # Row 2: 中指
  echo -en "$B$B$R$R$R$R$R$B" # Row 3: 拳頭上緣 (收起的指節)
  echo -en "$B$R$R$R$R$R$R$B" # Row 4: 手掌/拳頭
  echo -en "$B$R$R$R$R$R$R$B" # Row 5: 手掌
  echo -en "$B$B$R$R$R$R$B$B" # Row 6: 手腕/手掌基部
  echo -en "$B$B$B$B$B$B$B$B" # Row 7: 手腕
) > /dev/fb1

# 持續顯示 2 秒
sleep 2

# 初始化並熄滅所有 LED
dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null

