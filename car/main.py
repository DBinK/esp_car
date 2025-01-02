import time
import network
from machine import Pin

from modules.now import read_espnow
from modules.motion import RobotController
from modules.utils import map_value

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上


# 初始化 Omni Bot
robot = RobotController()

# 初始化 LED
led = Pin(46, Pin.OUT, value=1)

DEAD_AREA = 20  # 摇杆死区
MAP_COEFF = 58  # 摇杆映射系数 (根据实际需求调整)

while True:
    time.sleep(0.001)
    data = read_espnow()
    if data:

        lx = data[1]  
        ly = data[2]
        rx = data[3]
        ry = data[4]

        print(f"原始数据: lx={lx}, ly={ly}, rx={rx}, ry={ry}")

        lx += 16
        ly += 35
        rx += 16
        ry += 16

        print(f"矫正后数据: lx={lx}, ly={ly}, rx={rx}, ry={ry}")

        # 检查lx, ly, rx, ry中是否至少有一个绝对值超过设定值
        stick_work = (
               abs(lx-127) > DEAD_AREA
            or abs(ly-127) > DEAD_AREA
            or abs(rx-127) > DEAD_AREA
            or abs(ry-127) > DEAD_AREA
        )

        if stick_work:
            led.value(not led.value())  # 闪烁led

            # 底盘控制
            v_x = map_value(ly, (0, 255), (-100, 100))  if abs(ly-127) > DEAD_AREA else 0
            v_y = map_value(lx, (0, 255), (-100, 100))  if abs(lx-127) > DEAD_AREA else 0
            v_w = map_value(rx, (0, 255), (-100, 100))  if abs(rx-127) > DEAD_AREA else 0

            print(f"摇杆转速度 v_x={v_x}, v_y={v_y}, v_w={v_w}")

            v_x *= 0.8
            v_y *= 1.6
            v_w *= 0.8
            
            print(f"输入运动方程 v_x={v_x}, v_y={v_y}, v_w={v_w}")

            robot.move(v_x, -v_y, -v_w)  # 调用移动函数

        else:
            robot.move(0, 0, 0)
            led.value(0)