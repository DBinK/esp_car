# CRC8 实现
def crc8(data):
    crc = 0xFF  # 初始化 CRC 值
    polynomial = 0x31  # 多项式

    for byte in data:
        crc ^= byte  # 将当前字节与 CRC 值异或
        for _ in range(8):  # 处理每一位
            if crc & 0x80:  # 检查最高位
                crc = (crc << 1) ^ polynomial  # 左移并与多项式异或
            else:
                crc <<= 1  # 仅左移
            crc &= 0xFF  # 保持 CRC 在 8 位范围内

    return crc


if __name__ == "__main__":
    # 假设你的数据列表如下
    data = [0x00, 0x11, 0x23, 0x32, 0x1C, 0xAC, 0x23, 0x3F]

    # 计算校验位
    checksum = crc8(data)

    # 将校验位添加到列表的最后
    data.append(checksum)

    # 输出结果
    print("校验位:", checksum)
    print("数据列表:", data)