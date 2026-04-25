# 顏色定義：頭部(亮藍 \x1f\x00)、尾巴(深藍 \x0a\x00)
H='\x1f\x00'
T='\x0a\x00'

# 正中心 2x2 的像素索引：
# (3,3)=27, (4,3)=28, (4,4)=36, (3,4)=35
path=(27 28 36 35)

while true; do
    for ((i=0; i<4; i++)); do
        # 1. 清空螢幕
        dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
        
        # 2. 取得頭部與尾巴的索引
        idx_h=${path[i]}
        idx_t=${path[(i-1+4)%4]}

        # 3. 畫出頭部(亮)與尾巴(暗)
        echo -en "$T" | dd of=/dev/fb1 bs=1 seek=$((idx_t*2)) count=2 conv=notrunc 2>/dev/null
        echo -en "$H" | dd of=/dev/fb1 bs=1 seek=$((idx_h*2)) count=2 conv=notrunc 2>/dev/null

        # 2x2 路徑短，速度稍微調慢一點點比較清晰
        sleep 0.15
    done
done

