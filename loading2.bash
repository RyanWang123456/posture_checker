# 顏色定義：頭部(白色 \xff\xff)、身體(灰色 \x10\x84)、尾巴(深灰 \x08\x42)
HEAD='\xff\xff'
BODY='\x10\x84'
TAIL='\x08\x42'

# 內圈 4x4 的像素路徑 (索引值)
path=(18 19 20 21 29 37 45 53 52 51 50 49 41 33 25 17)
len=${#path[@]}

while true; do
    for ((i=0; i<len; i++)); do
        # 1. 清空緩衝區 (全黑)
        dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
        
        # 2. 取得頭部、身體、尾巴的索引
        idx_h=${path[i]}
        idx_b=${path[(i-1+len)%len]}
        idx_t=${path[(i-2+len)%len]}

        # 3. 依序畫出拖尾效果
        echo -en "$TAIL" | dd of=/dev/fb1 bs=1 seek=$((idx_t*2)) count=2 conv=notrunc 2>/dev/null
        echo -en "$BODY" | dd of=/dev/fb1 bs=1 seek=$((idx_b*2)) count=2 conv=notrunc 2>/dev/null
        echo -en "$HEAD" | dd of=/dev/fb1 bs=1 seek=$((idx_h*2)) count=2 conv=notrunc 2>/dev/null

        sleep 0.08
    done
done

