
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
def set_speed(rate):
    """
    设置电机的速度
    @param rate: 速度百分比，范围[-100, 100]
    """
    pwm_value = int(map_value(abs(rate), (0, 100), (0, 1023)))

    print(f"pwm_value: {pwm_value}")

set_speed(-20)