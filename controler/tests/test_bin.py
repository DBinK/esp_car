import struct

def list_to_binary_string(data_list):
    """
    将列表中的数据按分配好的空间转换成二进制字符串。

    参数:
    data_list (list): 包含8位无符号整数的列表。

    返回:
    str: 二进制字符串。
    """
    # 定义每个元素的格式，这里假设每个元素是一个8位无符号整数
    format_string = 'B' * len(data_list)

    # 将列表中的数据打包成二进制数据
    binary_data = struct.pack(format_string, *data_list)

    # 将二进制数据转换为整数，然后使用bin函数将其转换为二进制字符串
    binary_string = bin(int.from_bytes(binary_data, byteorder='big'))

    return binary_data

# 示例列表
data_list = [1, 2, 3, 4, 5]

# 调用函数并打印结果
binary_string = list_to_binary_string(data_list)
print(f"bin: {binary_string}")