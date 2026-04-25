# 顏色定義：亮藍色 (\x1f\x00)
C='\x1f\x00'

while true; do
    # 1. 第一波：第 1 欄 (2格)
    dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
    for i in 25 33; do echo -en "$C" | dd of=/dev/fb1 bs=1 seek=$((i*2)) count=2 conv=notrunc 2>/dev/null; done
    sleep 0.15

    # 2. 第二波：第 3 欄 (4格弧形)
    dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
    for i in 18 27 35 42; do echo -en "$C" | dd of=/dev/fb1 bs=1 seek=$((i*2)) count=2 conv=notrunc 2>/dev/null; done
    sleep 0.15

    # 3. 第三波：第 5 欄 (6格弧形)
    dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
    for i in 12 21 30 38 45 52; do echo -en "$C" | dd of=/dev/fb1 bs=1 seek=$((i*2)) count=2 conv=notrunc 2>/dev/null; done
    sleep 0.15

    # 4. 第四波：第 7 欄 (8格深弧形)
    # 路徑：(0,4)->(1,5)->(2,6)->(3,7)->(4,7)->(5,6)->(6,5)->(7,4)
    dd if=/dev/zero of=/dev/fb1 bs=128 count=1 2>/dev/null
    for i in 4 13 22 31 39 46 53 60; do echo -en "$C" | dd of=/dev/fb1 bs=1 seek=$((i*2)) count=2 conv=notrunc 2>/dev/null; done
    sleep 0.15
done

