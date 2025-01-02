"""
    Omni Bot 全向轮 运动控制模块
    by: DBin_K
"""

import time
import math
from machine import Pin, PWM  # type: ignore

from modules.utils import limit_value, map_value


class Motor:
    def __init__(self, forward_pin, backward_pin, PWM_LIMIT=(0, 1023)):
        """
        初始化电机对象
        @param speed_pin: 电机速度控制引脚
        @param dir_pin: 电机方向控制引脚
        @param PWM_LIMIT: PWM输出的上下限，默认为(0, 1023)
        """
        # 初始化电机控制对象
        self.PWM_LIMIT = PWM_LIMIT
        self.fw_speed = PWM(Pin(forward_pin), freq=500, duty=0)   # 速度控制引脚
        self.bk_speed = PWM(Pin(backward_pin), freq=500, duty=0)   # 速度控制引脚

    
    def set_speed(self, rate):
        """
        设置电机的速度
        @param rate: 速度百分比，范围[-100, 100]
        """
        pwm_value = int(map_value(abs(rate), (0, 100), self.PWM_LIMIT))
        pwm_value = limit_value(pwm_value, *self.PWM_LIMIT)  # 限制值

        if rate > 0:
            self.fw_speed.duty(pwm_value) 
            self.bk_speed.duty(0)

        elif rate < 0:
            self.fw_speed.duty(0)         
            self.bk_speed.duty(pwm_value)  

        else:
            self.fw_speed.duty(0)  
            self.bk_speed.duty(0) 


class RobotController:
    def __init__(self):
        self.motor_lf = Motor(21, 34)
        self.motor_lb = Motor(15, 16)  
        self.motor_rf = Motor(35, 36) 
        self.motor_rb = Motor(17, 18)  

    def scale_speed(self, v1, v2, v3, v4):
        """
        限制速度，确保每个输入电机的速度值不超过100, 且保证运动学解算结果准确
        """
        max_speed = 100  # 检查是否有速度超过最大值
        
        if abs(v1) > max_speed or abs(v2) > max_speed or abs(v3) > max_speed or abs(v4) > max_speed:
            
            max_current_speed = max(abs(v1), abs(v2), abs(v3), abs(v4))  # 计算当前速度的最大绝对值
            scale = max_speed / max_current_speed  # 计算缩放因子
            v1 *= scale  
            v2 *= scale
            v3 *= scale
            v4 *= scale
            
        return v1, v2, v3, v4  # 返回处理后的速度值

    def move(self, v_y, v_x, v_w): 
        """ 输入期望运动状态, 输出电机所需的运动速度 """

        # 运动学解算 
        v1 = v_y + v_x - v_w
        v2 = v_y - v_x - v_w
        v3 = v_y - v_x + v_w
        v4 = v_y + v_x + v_w

        # 限制速度
        v1, v2, v3, v4 = self.scale_speed(v1, v2, v3, v4)

        # 设置电机速度
        self.motor_lf.set_speed(v1)
        self.motor_lb.set_speed(v2)
        self.motor_rf.set_speed(v3)
        self.motor_rb.set_speed(v4)

    # 封装一些简单运动的控制方法
    def go_forward(self, rate):
        self.move(rate, 0, 0)

    def go_backward(self, rate):
        self.move(-rate, 0, 0)

    def go_left(self, rate):
        self.move(0, -rate, 0)

    def go_right(self, rate):
        self.move(0, rate, 0)

    def turn_left(self, rate):
        self.move(0, 0, rate)

    def turn_right(self, rate):
        self.move(0, 0, -rate)

    def stop(self):
        self.move(0, 0, 0)

    # 预留直接电机控制的方法
    def motor_lf_test(self, rate):
        self.motor_lf.set_speed(rate)

    def motor_lb_test(self, rate):
        self.motor_lb.set_speed(rate)

    def motor_rf_test(self, rate):
        self.motor_rf.set_speed(rate)

    def motor_rb_test(self, rate):
        self.motor_rb.set_speed(rate)


if __name__ == "__main__":

    import time

    robot = RobotController()


    print("测试rf轮")
    robot.motor_rf_test(50)
    time.sleep(3)
    robot.motor_rf_test(-50)
    time.sleep(3)
    robot.motor_rf_test(0)
    time.sleep(1)

    print("测试rb轮")
    robot.motor_rb_test(50)
    time.sleep(3)
    robot.motor_rb_test(-50)
    time.sleep(3)
    robot.motor_rb_test(0)
    time.sleep(1)

    print("测试lf轮")
    robot.motor_lf_test(50)
    time.sleep(3)
    robot.motor_lf_test(-50)
    time.sleep(3)
    robot.motor_lf_test(0)
    time.sleep(1)

    print("测试lb轮")
    robot.motor_lb_test(50)
    time.sleep(3)
    robot.motor_lb_test(-50)
    time.sleep(3)
    robot.motor_lb_test(0)
    time.sleep(1)
