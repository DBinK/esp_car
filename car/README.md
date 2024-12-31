# esp-omni-car 

使用 ESP32 制作的机器人 麦克纳姆轮底盘 控制程序

包含:

`boot.py` 一些单片机初始化的代码

`main.py` 主程序, 使用异步编程, 可同时接收 串口 和 ESP-NOW 的控制信号

`motion.py` 针对麦克纳姆轮底盘封装的运动控制类, 包含 电机类 和 编码器类

使用 MicroPython 编写