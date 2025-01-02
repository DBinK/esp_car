import time

def limit_value(value, min_value=-3000, max_value=3000):
    """限制输入的值在给定的范围内。"""
    return min(max(value, min_value), max_value)

def map_value(value, original_block, target_block):
    """将给定的值映射到给定的目标范围。"""
    original_min, original_max = original_block
    target_min, target_max = target_block
    # 计算映射后的值
    mapped_value = target_min + (value - original_min) * (target_max - target_min) / (original_max - original_min)

    return mapped_value

def time_diff(last_time=[None]):
    """计算两次调用之间的时间差，单位为微秒。"""
    current_time = time.ticks_us()  # 获取当前时间（单位：微秒）

    if last_time[0] is None:  # 如果是第一次调用，更新last_time
        last_time[0] = current_time
        return 0.000_001  # 防止除零错误

    else:  # 计算时间差
        diff = time.ticks_diff(current_time, last_time[0])  # 计算时间差
        last_time[0] = current_time  # 更新上次调用时间
        return diff  # 返回时间差us