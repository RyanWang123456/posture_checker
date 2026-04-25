# 顏色定義：綠色 (\xe0\x07)
C='\xe0\x07'

while true; do
    # 建立 128 bytes 的全黑畫布 (8x8 * 2 bytes)
    printf '\0%.0s' {1..128} > /tmp/frame

    for col in {0..7}; do
        # 隨機產生每一欄的高度 (1 到 8 格)
        height=$(( 1 + RANDOM % 8 ))
        
        # 根據高度畫出垂直線
        for ((row=7; row>7-height; row--)); do
            idx=$(( (row * 8) + col ))
            # 將顏色寫入畫布的特定偏移位置
            printf "$C" | dd of=/tmp/frame bs=1 seek=$((idx*2)) count=2 conv=notrunc 2>/dev/null
        done
    done

    # 一次性將畫布推送到 LED 矩陣，減少閃爍
    cat /tmp/frame > /dev/fb1
    sleep 0.1
done

